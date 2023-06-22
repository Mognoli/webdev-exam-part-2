from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from functools import wraps
from users_policy import UsersPolicy
import bleach
import markdown

bp = Blueprint('book', __name__, url_prefix='/book')

from app import db

LIST_PARAMS = ['name', 'year', 'publ_house', 'author', 'volume']

def params(names_list):
    result = {}
    for name in names_list:
        result[name] = request.form.get(name) or None
        if name == 'volume':
            result[name] = int(result[name])
            
    return result

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

def update_book(book_form):
    query = "UPDATE `books` SET `name` = %s, `short_desc` = %s, `year` = %s, `publ_house` = %s, `author` = %s, `volume` = %s WHERE `books`.`id` = %s;"
    try:
        with db.connection.cursor(named_tuple = True) as cursor:
          cursor.execute(query, (book_form.name, book_form.short_desc, book_form.year, book_form.publ_house, book_form.author, book_form.volume, book_form.id, ))
    except:
            db.connection.rollback()
            flash("При обновлении данных произошла ошибка", "danger")

    
def add_book(book_form):
    query = '''
    INSERT INTO `books` (`name`, `short_desc`, `year`, `publ_house`, `author`, `volume`) 
    VALUES (%(name)s, %(short_desc)s, %(year)s, %(publ_house)s, %(author)s, %(volume)s);
    '''
    with db.connection.cursor(named_tuple = True) as cursor:
        try:
            cursor.execute(query, (book_form))
            db.connection.commit()
            flash("Книга успешно добавлена", "success")
            return cursor.lastrowid
        except:
            db.connection.rollback()
            flash("При добавлении произошла ошибка", "danger")
    # query_serch = 'SELECT books.i'


def add_connection(id_book, id_genre):
    query = 'INSERT INTO `book_genre` (`book`, `genre`) VALUES (%s, %s);'
    with db.connection.cursor(named_tuple = True) as cursor:
        try:
            cursor.execute(query, (id_book, id_genre, ))
            db.connection.commit()
        except:
            db.connection.rollback()
            flash("При обновлении связи произошла ошибка", "danger")
    

@bp.route("/<int:book_id>/delete_book", methods=['POST'])
def delete_book(book_id):
    query = "DELETE FROM books WHERE books.id = %s"
    with db.connection.cursor(named_tuple = True) as cursor:
        try:
            cursor.execute(query, (book_id, ))
            db.connection.commit()
            flash("Книга успешно удалена", "success")
        except:
            db.connection.rollback()
            flash("При удалении произошла ошибка", "danger")
    return redirect(url_for("index"))

@bp.route("/<int:book_id>/show_book", methods=['POST', 'GET'])
def show_book(book_id):
    query = "SELECT * FROM books WHERE id = %s"
    with db.connection.cursor(named_tuple = True) as cursor:
        cursor.execute(query, (book_id, ))
        db_book = cursor.fetchone()
    short_desc = markdown.markdown(db_book.short_desc)
    list_genres = []
    genres = get_genre(book_id)
    for genre in genres:
        list_genres.append(genre.name)

    #загрузка обложки

    return render_template('book/show_book.html', book = db_book, list_genre = list_genres, short_desc = short_desc)

@bp.route("/new")
def new_book():
    genres = get_all_genre()
    return render_template('book/new.html', genres = genres)

@bp.route("/create_book", methods=['POST', 'GET'])
def create_book():
    # Основные параметры книги и ее добавление
    book_params = params(LIST_PARAMS)
    short_desc = request.form.get("short_desc") or None
    short_desc = bleach.clean(short_desc)
    book_params["short_desc"] = short_desc
    book_id = add_book(book_params)
    # Добавление жанров
    genres_list = request.form.getlist('genres')
    for genre in genres_list:
         add_connection(book_id, int(genre))

    return redirect(url_for("index"))