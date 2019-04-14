# coding:utf8
from . import home
from flask import render_template, flash, redirect, url_for, session, request
from app.home.forms import RegisterForm, LoginForm, AlterPwd, CommentForm, MessageForm
from app.models import User, UserLoginLog, Comment, Message, Link
import requests
from werkzeug.security import generate_password_hash
from app import db
import random
from functools import wraps
from app.models import Cate, Article

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
        userLoginLog = UserLoginLog(
            user_id=user.id,
            ip=request.remote_addr
        )
        db.session.add(userLoginLog)
        db.session.commit()
        return redirect(url_for('home.index', page=1))
    return render_template('home/login.html', form=loginForm)


@home.route('/logout/')
def logout():
    session.pop('user', None)
    return redirect(url_for('home.login'))


@home.route('/sourceCode/')
def sourceCode():
    return render_template('home/sourceCode.html')


@home.route('/technologyInfo/')
def technologyInfo():
    return render_template('home/technologyInfo.html')


@home.route('/disclaimer/')
def disclaimer():
    return render_template('home/disclaimer.html')


@home.route('/cooperation/')
def cooperation():
    return render_template('home/cooperation.html')


@home.route('/blueprint/')
def blueprint():
    return render_template('home/blueprint.html')


@home.route('/aboutWebmaster/')
def aboutWebmaster():
    return render_template('home/aboutWebmaster.html')


@home.route('/message/<int:page>', methods=['get', 'post'])
def message(page=None):
    messageForm = MessageForm()
    if messageForm.validate_on_submit():
        data = messageForm.data
        message = Message(
            content=data['content']
        )
        db.session.add(message)
        db.session.commit()
        flash('留言成功！', 'okey')
        return redirect(url_for('home.message', page=1))
    if page == None:
        page = 1
    pageData = Message.query.order_by(
        Message.addTime.desc()
    ).paginate(page=page, per_page=10)
    msgcount = Message.query.filter(
        Message.id
    ).count()
    return render_template('home/message.html', form=messageForm, pageData=pageData, msgcount=msgcount)


@home.route('/aboutUs/')
def aboutUs():
    return render_template('home/userAgreement.html')


@home.route('/')
def indexlTmp():
    return redirect(url_for('home.index', page=1))


@home.route("/<int:page>", methods=['get'])
def index(page=None):
    artCate = Cate.query.all()
    link = Link.query.all()
    if page is None:
        page = 1
    pageData = Article.query.order_by(
        Article.addTime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('home/index.html', pageData=pageData, artcate=artCate, link=link)


@home.route("/home/search/<int:page>", methods=['get'])
def searchArt(page=None):
    if page == None:
        page = 1
    key = request.args.get('keyWords', '')
    pageData = Article.query.filter(
        Article.title.ilike('%' + key + '%')
    ).order_by(
        Article.addTime.desc()
    ).paginate(page=page, per_page=10)
    artCount = Article.query.filter(
        Article.title.ilike('%' + key + '%')
    ).count()
    return render_template('home/search.html', key=key, pageData=pageData, count=artCount)


# 文章详细列表
@home.route("/art/desc/<int:id>/<int:page>", methods=['get', 'post'])
def artDesc(id=None, page=None):
    # art = Article.query.get_or_404(int(id))
    art = Article.query.join(
        Cate
    ).filter(
        Cate.id == Article.cate_id,
        Article.id == int(id)
    ).first_or_404()
    art.viewNum = art.viewNum + 1
    # 提交评论
    commentForm = CommentForm()
    if "user" in session and commentForm.validate_on_submit():
        data = commentForm.data
        comment = Comment(
            article_id=art.id,
            content=data['content'],
            user_id=session['id']
        )
        db.session.add(comment)
        db.session.commit()
        flash('评论成功！', 'okey')
        art.commentNum = art.commentNum + 1
    db.session.add(art)
    db.session.commit()
    if page == None:
        page = 1
    pageData = Comment.query.join(
        User
    ).join(
        Article
    ).filter(
        User.id == Comment.user_id,
        Article.id == Comment.article_id
    ).order_by(
        Comment.addTime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('home/artdesc.html', art=art, form=commentForm, pageData=pageData)


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
    page_data = UserLoginLog.query.order_by(
        UserLoginLog.addTime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('home/loginlog.html', page_data=page_data)


@home.route('/joke/', methods=['get'])
@userLoginRule
def joke():
    appkey = 'b863f6877d7e37cdc0f2e16177ab9c97'
    param = 'page=&pagesize=&key='
    url = 'http://v.juhe.cn/joke/content/text.php?' + param + appkey
    r = requests.get(url)
    data = r.json()
    return render_template('home/joke.html', data=data)
