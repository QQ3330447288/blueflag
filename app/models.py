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
    addTime = db.Column(db.DateTime, index=True, default=datetime.now)
    comment = db.relationship("Comment", backref='user')
    loginLog = db.relationship("UserLoginLog", backref='user')

    def check_pwd(self, pwd):
        return check_password_hash(self.pwd, pwd)


class UserLoginLog(db.Model):
    __tablename__ = 'userLoginLog'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ip = db.Column(db.String(20))
    addTime = db.Column(db.DateTime, index=True, default=datetime.now())


class Admin(db.Model):
    __tablename__ = "admin"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(50), unique=True)
    pwd = db.Column(db.String(100))
    is_super = db.Column(db.SmallInteger)
    role_id = db.Column(db.SmallInteger)
    addTime = db.Column(db.DateTime, default=datetime.now())

    def check_pwd(self, pwd):
        return check_password_hash(self.pwd, pwd)


# # 博文分类表
class Cate(db.Model):
    __tablename__ = 'cate'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 标题
    addTime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    articles = db.relationship("Article", backref='cate')  # 电影外键关系关联


# 博文表
class Article(db.Model):
    __tablename__ = "article"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(100), unique=True)  # 标题
    briefInfo = db.Column(db.Text)  # 简介
    cover = db.Column(db.String(255))  # 封面
    commentNum = db.Column(db.BigInteger, default=0)  # 评论量
    viewNum = db.Column(db.BigInteger, default=0)  # 查看量
    publisher = db.Column(db.String(50))
    addTime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    comment = db.relationship("Comment", backref='article')
    cate_id = db.Column(db.Integer, db.ForeignKey('cate.id'))  # 所属标签
    content = db.Column(db.Text)


class Comment(db.Model):
    __tablename__ = "comment"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))  # 所属博文
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    addTime = db.Column(db.DateTime, index=True, default=datetime.now)  # 评论时间


# 留言表
class Message(db.Model):
    __tablename__ = "message"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    addTime = db.Column(db.DateTime, index=True, default=datetime.now)  # 留言时间


# 权限表
class Auth(db.Model):
    __tablename__ = "auth"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(30), unique=True)  # 权限名称
    url = db.Column(db.String(255), unique=True)  # 权限地址
    addTime = db.Column(db.DateTime, index=True, default=datetime.now)


# 角色表
class Role(db.Model):
    __tablename__ = "role"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 角色名称
    auth = db.Column(db.String(600))  # 权限
    addTime = db.Column(db.DateTime, index=True, default=datetime.now)  # 角色添加时间


# 图片表
class Link(db.Model):
    __tablename__ = "link"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    first = db.Column(db.Text)
    second = db.Column(db.Text)
    third = db.Column(db.Text)
    forth = db.Column(db.Text)
    fifth = db.Column(db.Text)

# if __name__ == '__main__':
#     db.create_all()

# if __name__ == '__main__':
#     from werkzeug.security import generate_password_hash
#     print(generate_password_hash("wwwnxl"))
# pbkdf2:sha256:150000$uCnHQYQp$fd525ad25ecea3a2382c3a290a8fb0f5cf9e6c23b7328c96524d3b2066796f71
# admin = Admin(
#     account="Thanlon",
#     pwd=generate_password_hash("wwwnxl"),
#     is_super=0,
#     role_id=1
# )
# db.session.add(admin)
# db.session.commit()
