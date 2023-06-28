from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from functools import wraps
from users_policy import UsersPolicy
import bleach
import markdown
import math
from auth import check_rights

bp = Blueprint('review', __name__, url_prefix='/review')

from app import db

COUNT_REVIEW_ON_PAGE = 10

# Запросы к БД
def get_review(id_book):
    query = 'SELECT review.*, users.login AS user_name FROM review  LEFT JOIN users ON review.user=users.id WHERE review.book=%s AND review.statuses=2'
    with db.connection.cursor(named_tuple = True) as cursor:
        cursor.execute(query, (id_book, ))
        review_list = cursor.fetchall()
        value_reviews = len(review_list)
    return review_list, value_reviews

def check_review_user(book_id):
    query = 'SELECT count(*) AS count_review FROM review WHERE review.user=%s and review.book=%s'
    with db.connection.cursor(named_tuple = True) as cursor:
        cursor.execute(query, (current_user.id, book_id, ))
        count_review = cursor.fetchone().count_review
    if count_review == 0:
        return True
    else:
        return False

def add_review(review_form):
    query = '''
    INSERT INTO `review` (`book`, `user`, `grade`, `text_rew`, `statuses`) 
    VALUES (%(book)s, %(user)s, %(grade)s, %(text_rew)s, 1);'''
    with db.connection.cursor(named_tuple = True) as cursor:
        try:
            cursor.execute(query, (review_form))
            db.connection.commit()
        except:
            db.connection.rollback()
            flash("При создании рецензии произошла ошибка", "danger")

def get_review_id(id_review):
    query = 'SELECT review.*, users.login AS user_name, books.name AS book_name FROM review  LEFT JOIN users ON review.user=users.id LEFT JOIN books ON review.book=books.id WHERE review.id=%s'
    with db.connection.cursor(named_tuple = True) as cursor:
        cursor.execute(query, (id_review, ))
        review = cursor.fetchone()
    return review

def ger_review_user(user_id):
    query = '''
    SELECT review.*, books.name AS book_name, statuses.name AS statuses_name 
    FROM review  LEFT JOIN books ON review.book=books.id LEFT JOIN statuses
     ON review.statuses=statuses.id WHERE review.user=%s ORDER BY review.created_at DESC
    LIMIT %s OFFSET %s
    '''
    with db.connection.cursor(named_tuple = True) as cursor:
        cursor.execute(query, (user_id, ))
        review = cursor.fetchone()
    return review

    
# Метод для создания рецензии
@bp.route("/<int:book_id>/create_review", methods=['POST'])
def create_review(book_id):
    grade = int(request.form.get('grade'))
    text_rew = request.form.get('text-rew')
    text_rew = bleach.clean(text_rew)
    review_form = {
        'book': book_id,
        'user': current_user.id,
        'grade': grade,
        'text_rew': text_rew,
    }
 
    add_review(review_form)

    return redirect(url_for('book.show_book', book_id=book_id))

# Страница с списком рецензий (модер)
@bp.route("review_moder",  methods=['POST', 'GET'])
@login_required
@check_rights("review_moder")
def review_moder():
    # Получение номера страницы
    page = request.args.get('page', 1, type=int)
    statues = request.args.get('statues', 0, type=int)

    # Запросы на рецензии и на их количество
    query = '''
    SELECT review.*, users.login AS user_name, books.name AS book_name, statuses.name AS statuses_name 
    FROM review  LEFT JOIN users ON review.user=users.id LEFT JOIN books 
    ON review.book=books.id LEFT JOIN statuses ON review.statuses=statuses.id ORDER BY review.created_at DESC
    LIMIT %s OFFSET %s
    '''
    query_sort = '''
    SELECT review.*, users.login AS user_name, books.name AS book_name, statuses.name AS statuses_name 
    FROM review  LEFT JOIN users ON review.user=users.id LEFT JOIN books 
    ON review.book=books.id LEFT JOIN statuses ON review.statuses=statuses.id WHERE review.statuses=%s ORDER BY review.created_at DESC
    LIMIT %s OFFSET %s
    '''
    all_count_review_query = '''
    SELECT count(*) as count_review FROM review 
    '''
    short_count_review_query = '''
    SELECT count(*) as count_review FROM review LEFT JOIN statuses ON review.statuses=statuses.id WHERE review.statuses=%s
    
    '''
    if request.method == "POST":
        statues = int(request.form.get('statues'))


    # Для самих рецензий
    with db.connection.cursor(named_tuple = True) as cursor:
        if statues == 0:
            cursor.execute(query, (COUNT_REVIEW_ON_PAGE, COUNT_REVIEW_ON_PAGE * (page - 1)))     
        else:
            statues_id = statues
            cursor.execute(query_sort, (statues_id, COUNT_REVIEW_ON_PAGE, COUNT_REVIEW_ON_PAGE * (page - 1)))
        review_list = cursor.fetchall()
    # Для количества
    with db.connection.cursor(named_tuple = True) as cursor:
        if statues == 0:
            cursor.execute(all_count_review_query)     
        else:
            statues_id = statues
            cursor.execute(short_count_review_query, (statues_id, ))
        count_review = cursor.fetchone().count_review

    # Количество страниц
    page_count = math.ceil(count_review / COUNT_REVIEW_ON_PAGE)
    return render_template("review/review_moder.html", review_list = review_list, count_review=count_review, page = page, page_count = page_count, statues = statues)

# Просмотр рецензии для модерации
@bp.route("/<int:review_id>")
@login_required
@check_rights("review_moder")
def show_review(review_id):
    review = get_review_id(review_id)
    text_rew = review.text_rew
    text_rew = markdown.markdown(text_rew)
    return render_template("review/show_review.html", review = review, text_rew = text_rew)

# Одобрение рецензии
@bp.route("/<int:review_id>/true")
@check_rights("review_moder")
def update_statuse_true(review_id):
    query = 'UPDATE `review` SET `statuses` = 2 WHERE `review`.`id` = %s;'
    with db.connection.cursor(named_tuple = True) as cursor:
        try:
            cursor.execute(query, (review_id, ))
            db.connection.commit()
            flash("Статус успешно обнавлен", "success")
        except:
            db.connection.rollback()
            flash("При обновлении статуса произошла ошибка", "danger")
    return redirect(url_for("review.review_moder"))

# Отклонение рецензии
@bp.route("/<int:review_id>/false")
@login_required
@check_rights("review_moder")
def update_statuse_false(review_id):
    query = 'UPDATE `review` SET `statuses` = 3 WHERE `review`.`id` = %s;'
    with db.connection.cursor(named_tuple = True) as cursor:
        try:
            cursor.execute(query, (review_id, ))
            db.connection.commit()
            flash("Статус успешно обнавлен", "success")
        except:
            db.connection.rollback()
            flash("При обновлении статуса произошла ошибка", "danger")
    return redirect(url_for("review.review_moder"))

# # Страница с списком рецензий (user)
@bp.route("/review_user",  methods=['POST', 'GET'])
@login_required
@check_rights("review_user")
def review_user():
    # Получение номера страницы
    page = request.args.get('page', 1, type=int)
    statues = request.args.get('statues', 0, type=int)
    # Запросы на рецензии и на их количество
    query = '''
    SELECT review.*, books.name AS book_name, statuses.name AS statuses_name 
    FROM review  LEFT JOIN users ON review.user=users.id LEFT JOIN books 
    ON review.book=books.id LEFT JOIN statuses ON review.statuses=statuses.id WHERE review.user=%s ORDER BY review.created_at DESC
    LIMIT %s OFFSET %s
    '''
    query_sort = '''
    SELECT review.*, users.login AS user_name, books.name AS book_name, statuses.name AS statuses_name 
    FROM review  LEFT JOIN users ON review.user=users.id LEFT JOIN books 
    ON review.book=books.id LEFT JOIN statuses ON review.statuses=statuses.id WHERE review.user=%s AND review.statuses=%s ORDER BY review.created_at DESC
    LIMIT %s OFFSET %s
    '''
    all_count_review_query = '''
    SELECT count(*) as count_review FROM review WHERE review.user=%s
    '''
    short_count_review_query = '''
    SELECT count(*) as count_review FROM review LEFT JOIN statuses ON review.statuses=statuses.id WHERE review.user=%s AND review.statuses=%s
    
    '''

    if request.method == "POST":
        statues = int(request.form.get('statues'))

    user_id = int(current_user.id)

    with db.connection.cursor(named_tuple = True) as cursor:
        if statues == 0:
            cursor.execute(query, (user_id, COUNT_REVIEW_ON_PAGE, COUNT_REVIEW_ON_PAGE * (page - 1)))     
        else:
            statues_id = statues
            cursor.execute(query_sort, (user_id, statues_id, COUNT_REVIEW_ON_PAGE, COUNT_REVIEW_ON_PAGE * (page - 1)))
        review_list = cursor.fetchall()
    
    
    # Для количества
    with db.connection.cursor(named_tuple = True) as cursor:
        if statues == 0:
            cursor.execute(all_count_review_query, (user_id, ))     
        else:
            statues_id = statues
            cursor.execute(short_count_review_query, (user_id, statues_id, ))
        count_review = cursor.fetchone().count_review

    # Количество страниц
    page_count = math.ceil(count_review / COUNT_REVIEW_ON_PAGE)
    return render_template("review/review_user.html", review_list = review_list, page = page, page_count = page_count, statues=statues, count_review=count_review)