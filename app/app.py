from flask import Flask, render_template, session, request, redirect, url_for, flash
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

PER_PAGE = 10

#Стартовая страница
@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    query = "SELECT * FROM books ORDER BY books.year DESC LIMIT %s OFFSET %s"
    query_all_book = "SELECT count(*) as page_count FROM books"
    with db.connection.cursor(named_tuple = True) as cursor:
        cursor.execute(query, (PER_PAGE, PER_PAGE * (page - 1)))
        db_books = cursor.fetchall()
    with db.connection.cursor(named_tuple = True) as cursor:
        cursor.execute(query_all_book)
        db_counter = cursor.fetchone().page_count
    genre_book = {}
    for book in db_books:
        list_genres = []
        genres = get_genre(book.id)
        for genre in genres:
            list_genres.append(genre.name)
        genre_book[book.id] = list_genres
    page_count = math.ceil(db_counter / PER_PAGE)
    return render_template('index.html', books = db_books, list_genre = genre_book, page = page, page_count = page_count)

# Для отображения обложек

