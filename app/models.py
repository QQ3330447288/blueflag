from datetime import datetime
from app import db
from werkzeug.security import check_password_hash


# user table
class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {"useexisting": True}
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
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    ip = db.Column(db.String(20))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())


# admin table
class Admin(db.Model):
    __table_args__ = {"useexisting": True}
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(50), unique=True)
    pwd = db.Column(db.String(100))
    is_super = db.Column(db.SmallInteger)
    role_id = db.Column(db.SmallInteger)
    addtime = db.Column(db.DateTime, default=datetime.now())

    def check_pwd(self, pwd):
        return check_password_hash(self.pwd, pwd)


# # 博文分类表
class Artcate(db.Model):
    __tablename__: "artcate"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 标题
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间


# # 博文表
class Article(db.Model):
    __tablename__: "article"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(100), unique=True)  # 标题
    briefInfo = db.Column(db.Text)  # 简介
    cover = db.Column(db.String(255))  # 封面
    artCateId = db.Column(db.SmallInteger)
    commentNum = db.Column(db.BigInteger)  # 评论量
    viewNum = db.Column(db.BigInteger)  # 查看量
    publisher = db.Column(db.String(50))
    addTime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间


# if __name__ == '__main__':
#     db.create_all()

# if __name__ == '__main__':
#     # 向Admin表添加数据
#     from werkzeug.security import generate_password_hash
#
#     admin = Admin(
#         account="Thanlon",
#         pwd=generate_password_hash("wwwnxl"),
#         is_super=0,
#         role_id=1
#     )
#     db.session.add(admin)
#     db.session.commit()
