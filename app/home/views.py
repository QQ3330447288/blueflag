from . import home
from flask import render_template


@home.route("/")
def index():
    return render_template('home/index.html')


@home.route('/user/')
def user():
    return render_template('home/user.html')


@home.route('/register/')
def register():
    return render_template('home/register.html')


@home.route('/pwd/')
def pwd():
    return render_template('home/pwd.html')


@home.route('/comment/')
def comment():
    return render_template('home/comment.html')


@home.route('/loginlog/')
def loginlog():
    return render_template('home/loginlog.html')
