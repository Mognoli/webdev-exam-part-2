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

# Страница с списком рецензий
@bp.route("review_moder")
@check_rights("review_moder")
def review_moder():
    # Получение номера страницы
    page = request.args.get('page', 1, type=int)
    # Запросы на рецензии и на их количество
    query = '''
    SELECT review.*, users.login AS user_name, books.name AS book_name 
    FROM review  LEFT JOIN users ON review.user=users.id LEFT JOIN books 
    ON review.book=books.id WHERE review.statuses=1 ORDER BY review.created_at DESC
    LIMIT %s OFFSET %s
    '''
    query_count_review = "SELECT count(*) as page_count FROM review"
    with db.connection.cursor(named_tuple = True) as cursor:
        cursor.execute(query, (COUNT_REVIEW_ON_PAGE, COUNT_REVIEW_ON_PAGE * (page - 1)))
        review_list = cursor.fetchall()
    with db.connection.cursor(named_tuple = True) as cursor:
        cursor.execute(query_count_review)
        db_counter = cursor.fetchone().page_count

    # Количество страниц
    page_count = math.ceil(db_counter / COUNT_REVIEW_ON_PAGE)
    return render_template("review/review_moder.html", review_list = review_list, page = page, page_count = page_count)

# Просмотр рецензии для модерации
@bp.route("/<int:review_id>")
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