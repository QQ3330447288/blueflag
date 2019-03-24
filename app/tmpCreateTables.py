from datetime import datetime
from app import db
from werkzeug.security import check_password_hash


class UserLoginlog(db.Model):
    __tablename__ = 'userloginlog'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    ip = db.Column(db.String(20))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())


# if __name__ == "__main__":
#     db.create_all()
