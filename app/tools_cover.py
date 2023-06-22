import hashlib
import uuid
import os
from werkzeug.utils import secure_filename
from app import db, app
from flask import flash

def add_cover(params):
    query = '''
    INSERT INTO `covers` (`name`, `mime_type`, `md5_hash`, `book`) 
    VALUES (%(name)s, %(mime_type)s, %(md5_hash)s, %(book));
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

def chek_cover(hash):
    query ="SELECT * FROM covers WHERE covers.md5_hash=%s"
    with db.connection.cursor(named_tuple = True) as cursor:
        try:
            cursor.execute(query, (hash, ))
            db.connection.commit()
        except:
            db.connection.rollback()



class CoverSaver:
    def __init__(self, file):
        self.file = file

    def save(self):
        self.img = self.__find_by_md5_hash()
        if self.img is not None:
            return self.img
        file_name = secure_filename(self.file.filename)
        self.img = Image(
            id=str(uuid.uuid4()),
            file_name=file_name,
            mime_type=self.file.mimetype,
            md5_hash=self.md5_hash)
        self.file.save(
            os.path.join(app.config['UPLOAD_FOLDER'],
                         self.img.storage_filename))
        db.session.add(self.img)
        db.session.commit()
        return self.img

    def __find_by_md5_hash(self):
        self.md5_hash = hashlib.md5(self.file.read()).hexdigest()
        self.file.seek(0)
        return db.session.execute(db.select(Image).filter(Image.md5_hash == self.md5_hash)).scalar()
