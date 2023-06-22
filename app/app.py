from flask import Flask, render_template, session, request, redirect, url_for, flash, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from mysql_db import MySQL
import mysql.connector
import math

app = Flask(__name__)
aplication = app

app.config.from_pyfile('config.py')
db = MySQL(app)

# Регистрация Blueprint для разделения кода
# Все что связано с авторизацией
from auth import bp as bp_auth, init_login_manager, check_rights
init_login_manager(app)
app.register_blueprint(bp_auth)
# Все что связано с книгами
from book import bp as bp_book, get_genre
app.register_blueprint(bp_book)
# Рецензии
from review import bp as review
app.register_blueprint(review)

PER_PAGE = 10

#Стартовая страница
@app.route('/')
def index():
    # Получение страницы
    page = request.args.get('page', 1, type=int)
    # Запросы на на книги и на их количество
    query = "SELECT * FROM books ORDER BY books.year DESC LIMIT %s OFFSET %s"
    query_all_book = "SELECT count(*) as page_count FROM books"
    with db.connection.cursor(named_tuple = True) as cursor:
        cursor.execute(query, (PER_PAGE, PER_PAGE * (page - 1)))
        db_books = cursor.fetchall()
    with db.connection.cursor(named_tuple = True) as cursor:
        cursor.execute(query_all_book)
        db_counter = cursor.fetchone().page_count
    # Получение жанров
    genre_book = {}
    for book in db_books:
        list_genres = []
        genres = get_genre(book.id)
        for genre in genres:
            list_genres.append(genre.name)
        genre_book[book.id] = list_genres
    # Количество страниц
    page_count = math.ceil(db_counter / PER_PAGE)
    return render_template('index.html', books = db_books, list_genre = genre_book, page = page, page_count = page_count)

# Поиск обложки
def cover_bd(cover_id):
    query ='SELECT covers.* FROM covers WHERE covers.id=%s'
    with db.connection.cursor(named_tuple = True) as cursor:
        cursor.execute(query, (cover_id, ))
        this_cover = cursor.fetchall()[0]
    return this_cover

# Для отображения обложек
@app.route('/images/<cover_id>')
def cover(cover_id):
    cover = cover_bd(cover_id)
    name_file = str(cover.id) + '.' + str(cover.mime_type)
    return send_from_directory(app.config['UPLOAD_FOLDER'], name_file)

