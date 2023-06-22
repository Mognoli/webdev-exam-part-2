from flask_login import current_user

class UsersPolicy:
    def __init__(self, record):
        self.record = record

    def create(self):
        return current_user.is_admin()

    def show(self):
        return True

    def delete(self):
        return current_user.is_admin()

    def edit(self):
        if current_user.is_moder() or current_user.is_admin():
            return True
        return False
    
    def review_moder(self):
        if current_user.is_moder():
            return True
        return False
    