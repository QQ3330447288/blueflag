from datetime import datetime
from app import db
from werkzeug.security import check_password_hash


# user table
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(11), unique=True)
    info = db.Column(db.Text)  # personal introduce
    face = db.Column(db.String(255), unique=True)  # face
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    uuid = db.Column(db.String(255), unique=True)  # uuid

    def __repr__(self):
        return "<User %r>" % self.name

    def check_pwd(self, pwd):
        return check_password_hash(self.pwd, pwd)


class UserLoginlog(db.Model):
    __tablename__ = 'userloginlog'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    ip = db.Column(db.String(20))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())
# if __name__ == "__main__":
#     db.create_all()#create  all tables
