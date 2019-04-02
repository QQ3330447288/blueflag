from . import admin
from app.admin.forms import LoginForm, ArtCateForm, ArtForm
from flask import render_template, flash, redirect, url_for, session, request
from functools import wraps
from app.models import Admin, Artcate, Article
from app import db
from werkzeug.utils import secure_filename
import os, datetime, uuid
from app import app


# 定义装饰器
def adminLoginRule(f):
    @wraps(f)
    def decoratedFunction(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for('admin.login', next=request.url))
        return f(*args, **kwargs)

    return decoratedFunction


@admin.route('/thanlon/login', methods=['get', 'post'])
def login():
    loginForm = LoginForm()
    loginData = loginForm.data
    if loginForm.validate_on_submit():
        admin = Admin.query.filter_by(account=loginData['account']).first()
        if not admin.check_pwd(loginData['pwd']):
            flash('密码有误，请重新输入!', 'error')
            return redirect(url_for('admin.login'))
        session['admin'] = loginData['account']
        return redirect(url_for('admin.index'))
    return render_template('admin/login.html', form=loginForm)


@admin.route('/admin/logout/')
def logout():
    session.pop('admin', None)
    return redirect(url_for('admin.login'))


@admin.route('/thanlon/', methods=['get', 'post'])
@adminLoginRule
def index():
    return render_template('admin/index.html')


@admin.route('/admin/addArtCate', methods=['get', 'post'])
@adminLoginRule
def addArtCate():
    artCateForm = ArtCateForm()
    data = artCateForm.data
    if artCateForm.validate_on_submit():
        artCateCount = Artcate.query.filter_by(name=data['name']).count()
        if artCateCount >= 1:
            flash('标签已经存在！', 'error')
            return redirect(url_for('admin.addTag'))
        cate = Artcate(
            name=data["name"]
        )
        db.session.add(cate)
        db.session.commit()
        flash("添加标签成功！", "okey")
        redirect(url_for("admin.addArtCate"))
    return render_template('admin/addArtCate.html', form=artCateForm)


@admin.route('/admin/artCate/list/<int:page>', methods=['get'])
@adminLoginRule
def artCateList(page=None):
    if page == None:
        page = 1
    pageData = Artcate.query.order_by(
        Artcate.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/artCateList.html', pageData=pageData)


# 修改文件名称
def change_filename(filename):  # 需要将filename转换为安全的文件爱你名称（filename）有时间前缀字符串拼接的名称
    file_info = os.path.splitext(filename)  # 分割成后缀加前缀
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + file_info[-1]
    return filename


@admin.route('/admin/addArt/', methods=['get', 'post'])
@adminLoginRule
def addArt():
    artForm = ArtForm()

    if artForm.validate_on_submit():
        data = artForm.data
        filecover = secure_filename(artForm.cover.data.filename)

        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")

        cover = change_filename(filecover)

        artForm.cover.data.save(app.config["UP_DIR"] + cover)

        art = Article(
            title=data['title'],
            briefInfo=data['briefInfo'],
            cover=cover,
            artCateId=int(data['artCateId']),
            publisher=session['admin']
        )
        db.session.add(art)
        db.session.commit()
        flash("添加标签成功！", "okey")
        redirect(url_for("admin.addArt"))
    return render_template('admin/addArt.html', form=artForm)


@admin.route('/admin/art/list', methods=['get', 'post'])
@adminLoginRule
def ArtList():
    return render_template('admin/artList.html')
