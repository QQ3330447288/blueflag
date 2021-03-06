from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)  # parameter is application's models or package's name;initialize class

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:wwwnxl@localhost:3306/blueflag?charset=utf8"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["SECRET_KEY"] = '0160a068dba74c5aa21f5b93cc6b95c5'
db = SQLAlchemy(app)

# 定义一个文件上传保存路径
app.config["UP_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/articles/")

from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

app.debug = True
# regist blueprint
app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint)


@app.errorhandler(404)
def page_not_find(error):
    return render_template("home/404.html"), 404
