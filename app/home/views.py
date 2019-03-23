from . import home
from flask import render_template, flash, redirect, url_for, session
from app.home.forms import RegisterForm
from app.models import User
import requests
from werkzeug.security import generate_password_hash
import uuid
from app import db
import random
import re

randomCode = str(random.randint(1000, 9999))


@home.route('/register/', methods=['get', 'post'])
def register():
    registerForm = RegisterForm()
    if registerForm.validate_on_submit():
        formData = registerForm.data
        # print(formData)
        # print(type(randomCode))
        # print(type(formData['code']))
        if randomCode == formData['code']:
            # print("okey!")
            user = User(
                name=formData['name'],
                pwd=generate_password_hash(formData['pwd']),
                phone=formData['phone']
            )
            db.session.add(user)
            db.session.commit()
            flash('注册成功！', 'okey')
        else:
            flash('注册失败,请检查验证码是否正确输入！', 'error')
    return render_template('home/register.html', form=registerForm)


@home.route('/sendCode/', methods=['get', 'post'])
def sendCode():
    registerForm = RegisterForm()
    formData = registerForm.data
    phone = formData['phone']
    req_url = "http://api.feige.ee/SmsService/Send"
    data = {"Account": "18937693205", "Pwd": "1593820c5e67784b988976748", "Content": "验证码:" + randomCode,
            "Mobile": phone, "SignId": 106861}
    response = requests.post(req_url, data=data)
    return redirect(url_for('home.register'))


@home.route('/login/')
def login():
    return render_template('home/login.html')


@home.route('/sourceCode/')
def sourceCode():
    return render_template('home/sourceCode.html')


@home.route('/disclaimer/')
def disclaimer():
    return render_template('home/disclaimer.html')


@home.route('/cooperation/')
def cooperation():
    return render_template('home/cooperation.html')


@home.route('/blueprint/')
def blueprint():
    return render_template('home/blueprint.html')


@home.route('/aboutUs/')
def aboutUs():
    return render_template('home/userAgreement.html')


@home.route("/")
def index():
    return render_template('home/index.html')


@home.route('/user/')
def user():
    return render_template('home/user.html')


@home.route('/pwd/')
def pwd():
    return render_template('home/pwd.html')


@home.route('/comment/')
def comment():
    return render_template('home/comment.html')


@home.route('/loginlog/')
def loginlog():
    return render_template('home/loginlog.html')
