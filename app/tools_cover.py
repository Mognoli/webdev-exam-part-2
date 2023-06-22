import hashlib
import os
from werkzeug.utils import secure_filename
from app import db, app
from flask import flash

# Поиск изображения по id
def select_cover(cover_id):
    query ="SELECT * FROM covers WHERE covers.id=%s"
    with db.connection.cursor(named_tuple = True) as cursor:
        try:
            cursor.execute(query, (cover_id, ))
            db_cover = cursor.fetchall()[0]
            return db_cover
        except:
            db.connection.rollback()

# Добавление обложки в БД
def add_cover(params):
    query = '''
    INSERT INTO `covers` (`name`, `mime_type`, `md5_hash`) 
    VALUES (%(name)s, %(mime_type)s, %(md5_hash)s);
    '''
    with db.connection.cursor(named_tuple = True) as cursor:
        try:
            cursor.execute(query, (params))
            db.connection.commit()
            flash("Обложка успешно добавлена", "success")
            return cursor.lastrowid
        except:
            db.connection.rollback()
            flash("При добавлении произошла ошибка", "danger")

# Удаление обложки из БД
def delet_cover(id_cover):
    query = "DELETE FROM covers WHERE covers.id = %s"
    with db.connection.cursor(named_tuple = True) as cursor:
        try:
            cursor.execute(query, (id_cover, ))
            db.connection.commit()
            flash("Обложка успешно удалена", "success")
        except:
            db.connection.rollback()
            flash("При удалении произошла ошибка", "danger")

# Проверка существованя обложки с хешем
def chek_cover(hash):
    query ="SELECT * FROM covers WHERE covers.md5_hash=%s"
    with db.connection.cursor(named_tuple = True) as cursor:
        try:
            cursor.execute(query, (hash, ))
            db_cover = cursor.fetchall()[0]
            return db_cover
        except:
            db.connection.rollback()

# Проверка существования книги с обложкой
def chek_cover_book(cover_id):
    query ="SELECT * FROM books WHERE books.cover=%s"
    with db.connection.cursor(named_tuple = True) as cursor:
        try:
            cursor.execute(query, (cover_id, ))
            db_book = cursor.fetchall()[0]
            return db_book
        except:
            db.connection.rollback()

class CoverSaver:
    def __init__(self, file):
        self.file = file

    # Сохранение обложки
    def save(self):
        self.cover = self.__find_by_md5_hash()
        if self.cover is not None:
            return self.cover.id
        file_name = secure_filename(self.file.filename)
        mimetype = file_name.split('.')[1]
        params_to_db = {
            "md5_hash": self.md5_hash,
            "name": file_name,
            "mime_type": mimetype,
        }
        id_cover = add_cover(params_to_db)
        storage_name = str(id_cover) + '.' + mimetype
        self.file.save(os.path.join(app.config['UPLOAD_FOLDER'], storage_name))
        return id_cover

    # Поиск хеша
    def __find_by_md5_hash(self):
        self.md5_hash = hashlib.md5(self.file.read()).hexdigest()
        self.file.seek(0)
        return chek_cover(self.md5_hash)

# Удаление обложки 
def delete_cover(cover_id):
    book_cover = chek_cover_book(cover_id)
    if not book_cover:
        cover = select_cover(cover_id)
        storage_name = str(cover.id) + '.' + cover.mime_type
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], storage_name))
        delet_cover(cover_id)
