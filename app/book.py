from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from functools import wraps
from users_policy import UsersPolicy
import bleach
import markdown
from tools_cover import CoverSaver, delete_cover
from review import get_review, check_review_user
from auth import check_rights

bp = Blueprint('book', __name__, url_prefix='/book')

from app import db

LIST_PARAMS = ['name', 'year', 'publ_house', 'author', 'volume']

# Получение параметров
def params(names_list):
    result = {}
    for name in names_list:
        result[name] = request.form.get(name)
        if result[name] and name == 'volume' and result[name].isdigit():
            result[name] = int(result[name])
            
    return result

# Запросы к БД
def get_all_genre():
    query = "SELECT * FROM genres"
    with db.connection.cursor(named_tuple = True) as cursor:
        cursor.execute(query)
        genre_book = cursor.fetchall()
    return genre_book

def get_genre(id_book):
    query = "SELECT genres.* FROM book_genre LEFT JOIN genres on book_genre.genre = genres.id WHERE book_genre.book = %s"
    with db.connection.cursor(named_tuple = True) as cursor:
        cursor.execute(query, (id_book, ))
        genre_book = cursor.fetchall()
    return genre_book

def delete_connection(id_book):
    query = "DELETE FROM book_genre WHERE book_genre.book = %s"
    with db.connection.cursor(named_tuple = True) as cursor:
        try:
            cursor.execute(query, (id_book, ))
            db.connection.commit()
        except:
            db.connection.rollback()

def add_connection(id_book, id_genre):
    query = 'INSERT INTO `book_genre` (`book`, `genre`) VALUES (%s, %s);'
    with db.connection.cursor(named_tuple = True) as cursor:
        try:
            cursor.execute(query, (id_book, id_genre, ))
            db.connection.commit()
        except:
            db.connection.rollback()
            flash("При обновлении связи произошла ошибка", "danger")
    
# Запрос на удаление книги
@bp.route("/<int:book_id>/delete_book", methods=['POST'])
@login_required
@check_rights("delete")
def delete_book(book_id):
    query_for_cover = 'SELECT * FROM books WHERE books.id=%s'
    with db.connection.cursor(named_tuple = True) as cursor:
        cursor.execute(query_for_cover, (book_id, ))
        this_book = cursor.fetchall()[0]
    cover_id = this_book.cover
    delete_cover(cover_id)
    query = "DELETE FROM books WHERE books.id = %s"
    with db.connection.cursor(named_tuple = True) as cursor:
        try:
            cursor.execute(query, (book_id, ))
            db.connection.commit()
            flash("Книга успешно удалена", "success")
        except:
            db.connection.rollback()
            flash("При удалении книги произошла ошибка", "danger")
    return redirect(url_for("index"))

@bp.route("/<int:book_id>/show_book")
@login_required
@check_rights("show")
def show_book(book_id):
    # Книга
    query = "SELECT * FROM books WHERE id = %s"
    with db.connection.cursor(named_tuple = True) as cursor:
        cursor.execute(query, (book_id, ))
        db_book = cursor.fetchone()
    # Описание и переделывание в html 
    short_desc = markdown.markdown(db_book.short_desc)
    # Подгрузка жанров книги
    list_genres = []
    genres = get_genre(book_id)
    for genre in genres:
        list_genres.append(genre.name)
    # Рецензии
    review_list, value_reviews = get_review(book_id)
    text_rew_list = {}
    for review in review_list:
        text_rew_list[review.id] = markdown.markdown(review.text_rew)
    check_review = check_review_user(book_id)
    return render_template('book/show_book.html', 
                           book = db_book, list_genre = list_genres, 
                           short_desc = short_desc, review_list = review_list, 
                           text_rew_list = text_rew_list, value_reviews = value_reviews, 
                           check_review = check_review)

# ошибка при добавлении книги
def error_create(book_genres, book_info):
    all_genres = get_all_genre()
    return render_template('book/new.html', genres = all_genres, book_genres = book_genres, book_info = book_info)

@bp.route("/new", methods=['POST', 'GET'])
@login_required
@check_rights("create")
def new_book():
    if request.method == "POST":
        # Основные параметры книги и ее добавление
        book_params = params(LIST_PARAMS)
        genres_list_str = request.form.getlist('genres')
        genres_list_int = []
        for genre in genres_list_str:
            genres_list_int.append(int(genre))

        # Работа с описанием 
        short_desc = request.form.get("short_desc")
        if not short_desc:
                flash("При добавлении книги произошла ошибка", "danger")
                return error_create(genres_list_int, book_params)
        short_desc = bleach.clean(short_desc)
        book_params["short_desc"] = short_desc

        # Добавление обложек
        f = request.files.get('background_img')
        if f and f.filename:
            cover = CoverSaver(f).save()
        else:
            flash("При добавлении книги произошла ошибка", "danger")
            return error_create(genres_list_int, book_params)

        # Проверка на то что все поля есть
        for param in LIST_PARAMS:
            if not book_params[param]:
                flash("При добавлении книги произошла ошибка", "danger")
                return error_create(genres_list_int, book_params)

        if not genres_list_int:
            flash("При добавлении книги произошла ошибка", "danger")
            return error_create(genres_list_int, book_params)

        book_params["cover"] = cover

        # Добавление книги
        query = '''
        INSERT INTO `books` (`name`, `short_desc`, `year`, `publ_house`, `author`, `volume`, `cover`) 
        VALUES (%(name)s, %(short_desc)s, %(year)s, %(publ_house)s, %(author)s, %(volume)s, %(cover)s);
        '''
        with db.connection.cursor(named_tuple = True) as cursor:
            try:
                cursor.execute(query, (book_params))
                db.connection.commit()
                flash("Книга успешно добавлена", "success")
                book_id = cursor.lastrowid
            except:
                db.connection.rollback()
                flash("При добавлении произошла ошибка", "danger")
                return error_create(genres_list_int, book_params)

        # Добавление жанров
        for genre in genres_list_int:
            add_connection(book_id, genre)

        return redirect(url_for("index"))
    
    # Метод GET = 1ая  загрузка страницы
    genres = get_all_genre()
    return render_template('book/new.html', genres = genres, book_genres = {}, book_info = {})

# Ошибка при изменении книги
def error_edit(book_genres, book_info):
    all_genres = get_all_genre()
    return render_template('book/edit.html', genres = all_genres, book_genres = book_genres, book_info = book_info)

@bp.route("/<int:book_id>/edit", methods=['POST', 'GET'])
@login_required
@check_rights("edit")
def edit_book(book_id):
    if request.method == "POST":
        # Основные параметры и жанры
        book_params = params(LIST_PARAMS)
        genres_list_str = request.form.getlist('genres')
        genres_list_int = []
        for genre in genres_list_str:
            genres_list_int.append(int(genre))

        # Работа с описанием
        short_desc = request.form.get("short_desc")
        if not short_desc:
                flash("При обнавлении книги произошла ошибка", "danger")
                return error_edit(genres_list_int, book_params)
        short_desc = bleach.clean(short_desc)
        book_params["short_desc"] = short_desc
        book_params["id"] = book_id

        # Проверка наличия всех параметров
        for param in LIST_PARAMS:
            if not book_params[param]:
                flash("При обнавлении книги произошла ошибка", "danger")
                return error_edit(genres_list_int, book_params)

        if not genres_list_int:
            flash("При обнавлении книги произошла ошибка", "danger")
            return error_edit(genres_list_int, book_params)

        # Изменение жанров
        delete_connection(book_id)
        for genre in genres_list_int:
             add_connection(book_id, genre)

        # Изменение информации о книге
        query = '''
        UPDATE `books` SET `name` = %(name)s, `short_desc` = %(short_desc)s, `year` = %(year)s, 
        `publ_house` = %(publ_house)s, `author` = %(author)s, `volume` = %(volume)s WHERE `books`.`id` = %(id)s;'''
        with db.connection.cursor(named_tuple = True) as cursor:
            try:
                cursor.execute(query, (book_params))
                db.connection.commit()
                flash("Книга успешно обнавлена", "success")
            except:
                db.connection.rollback()
                flash("При обновлении данных произошла ошибка", "danger")
                return error_edit(genres_list_int, book_params)

        return redirect(url_for("index"))

    # Метод GET = 1ая  загрузка страницы
    query = "SELECT * FROM books WHERE id = %s"
    with db.connection.cursor(named_tuple = True) as cursor:
        cursor.execute(query, (book_id, ))
        db_book = cursor.fetchone()
    book_genres = []
    genres = get_genre(book_id)
    for genre in genres:
        book_genres.append(genre.id)

    all_genres = get_all_genre()
    return render_template('book/edit.html', genres=all_genres, book_genres = book_genres, book_info = db_book)