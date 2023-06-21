from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from functools import wraps
from users_policy import UsersPolicy

bp = Blueprint('book', __name__)

from app import db

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
    query = 'INSERT INTO `books` (`id`, `name`, `short_desc`, `year`, `publ_house`, `author`, `volume`) VALUES (NULL, %s, %s, %s, %s, %s, %s);' 
    with db.connection.cursor(named_tuple = True) as cursor:
        try:
            cursor.execute(query, (book_form.name, book_form.short_desc, book_form.year, book_form.publ_house, book_form.author, book_form.volume, ))
        except:
                db.connection.rollback()
                flash("При добавлении произошла ошибка", "danger")

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
    list_genres = []
    genres = get_genre(book_id)
    for genre in genres:
        list_genres.append(genre.name)

    #загрузка обложки

    return render_template('show_book.html', book = db_book, list_genre = list_genres)

@bp.route("/create_book", methods=['POST', 'GET'])
def create_book():
    

    return render_template('book/form.html')