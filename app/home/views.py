from . import home
from flask import render_template, flash, redirect, url_for, session, request
from app.home.forms import RegisterForm, LoginForm, AlterPwd
from app.models import User, UserLoginlog
import requests
from werkzeug.security import generate_password_hash
from app import db
import random
from functools import wraps

randomCode = str(random.randint(1000, 9999))


def userLoginRule(f):
    @wraps(f)
    def decoratedFunction(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('home.login', next=request.url))
        return f(*args, **kwargs)

    return decoratedFunction


@home.route('/register/', methods=['get', 'post'])
def register():
    registerForm = RegisterForm()
    if registerForm.validate_on_submit():
        formData = registerForm.data
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
    data = {"Account": "18937693205", "Pwd": "1593820c5e67784b988976748",
            "Content": "验证码:" + randomCode + "。此验证码仅用于校验身份以注册和登录到蓝色旗帜网，10分钟内有效。",
            "Mobile": phone, "SignId": 106861}
    response = requests.post(req_url, data=data)
    return redirect(url_for('home.register'))


@home.route('/login/', methods=['get', 'post'])
def login():
    loginForm = LoginForm()
    loginData = loginForm.data
    if loginForm.validate_on_submit():
        user = User.query.filter_by(name=loginData['name']).first()
        if not user.check_pwd(loginData['pwd']):
            flash('密码有误，请重新输入!', 'error')
            redirect(url_for('home.login'))
        session['user'] = user.name
        session['id'] = user.id
        userLoginLog = UserLoginlog(
            user_id=user.id,
            ip=request.remote_addr
        )
        db.session.add(userLoginLog)
        db.session.commit()
        return redirect(url_for('home.index'))
    return render_template('home/login.html', form=loginForm)


@home.route('/logout/')
def logout():
    session.pop('user', None)
    return redirect(url_for('home.login'))


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
@userLoginRule
def user():
    return render_template('home/user.html')


@home.route('/alterpwd/', methods=['get', 'post'])
@userLoginRule
def alterpwd():
    alterpwdForm = AlterPwd()
    alterPwdDate = alterpwdForm.data
    if alterpwdForm.validate_on_submit():
        user = User.query.filter_by(name=session['user']).first()
        user.pwd = generate_password_hash(alterPwdDate['newPwd'])
        db.session.add(user)
        db.session.commit()
        flash('修改密码成功，您需要重新登录！', 'okey')
        return redirect(url_for('home.logout'))
    return render_template('home/alterpwd.html', form=alterpwdForm)


@home.route('/comment/')
@userLoginRule
def comment():
    return render_template('home/comment.html')


@home.route('/loginlog/<int:page>', methods=['get'])
@userLoginRule
def loginlog(page=None):
    if page is None:
        page = 1
    page_data = UserLoginlog.query.order_by(
        UserLoginlog.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('home/loginlog.html', page_data=page_data)
