# coding:utf8
from . import admin
from app.admin.forms import LoginForm, ArtCateForm, ArtForm, AuthForm, RoleForm, AdminForm, LinkForm, NewsCateForm, \
    NewsForm
from flask import render_template, flash, redirect, url_for, session, request
from functools import wraps
from app.models import Admin, Cate, Article, User, Auth, Role, Link, Message, Comment, NewsCate, News
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


# 定义装饰器
def adminAuth(f):
    @wraps(f)
    def decoratedFunction(*args, **kwargs):
        return f(*args, **kwargs)

    return decoratedFunction


# 修改文件名称
def change_filename(filename):  # 需要将filename转换为安全的文件爱你名称（filename）有时间前缀字符串拼接的名称
    file_info = os.path.splitext(filename)  # 分割成后缀加前缀
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + file_info[-1]
    return filename


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
        artCateCount = Cate.query.filter_by(name=data['name']).count()
        if artCateCount >= 1:
            flash('标签已经存在！', 'error')
            return redirect(url_for('admin.addTag'))
        cate = Cate(
            name=data["name"]
        )
        db.session.add(cate)
        db.session.commit()
        flash("添加标签成功！", "okey")
        redirect(url_for("admin.addArtCate"))
    return render_template('admin/addArtCate.html', form=artCateForm)


@admin.route('/admin/ArtCate/del/<int:id>', methods=['get', 'post'])
@adminLoginRule
def delArtCate(id=None):
    artcate = Cate.query.filter_by(
        id=id
    ).first_or_404()
    db.session.delete(artcate)
    db.session.commit()
    flash("删除文章分类列表成功！", "okey")
    return redirect(url_for("admin.artCateList", page=1))


@admin.route('/admin/artCate/list/<int:page>', methods=['get'])
@adminLoginRule
def artCateList(page=None):
    if page == None:
        page = 1
    pageData = Cate.query.order_by(
        Cate.addTime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/artCateList.html', pageData=pageData)


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
            cate_id=int(data['artCateId']),
            publisher=session['admin'],
            content=data['content'],
        )
        db.session.add(art)
        db.session.commit()
        flash("发布文章成功!", "okey")
        redirect(url_for("admin.addArt"))
    return render_template('admin/addArt.html', form=artForm)


@admin.route('/admin/Art/del/<int:id>', methods=['get', 'post'])
@adminLoginRule
def delArt(id=None):
    art = Article.query.filter_by(
        id=id
    ).first_or_404()
    db.session.delete(art)
    db.session.commit()
    flash("删除文章列表成功！", "okey")
    return redirect(url_for("admin.ArtList", page=1))


@admin.route('/admin/art/list/<int:page>', methods=['get'])
@adminLoginRule
def ArtList(page=None):
    if page == None:
        page = 1
    pageData = Article.query.join(
        Cate
    ).filter(
        Article.cate_id == Cate.id
    ).order_by(
        Article.addTime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/artList.html', pageData=pageData)


# 会员信息列表
@admin.route('/admin/user/list/<int:page>', methods=['get'])
@adminLoginRule
def userList(page=None):
    if page == None:
        page = 1
    pageData = User.query.order_by(
        User.addTime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/userList.html', pageData=pageData)


# 添加权限
@admin.route('/admin/auth/add/', methods=['get', 'post'])
@adminLoginRule
def addAuth():
    authForm = AuthForm()
    form = AuthForm()
    if form.validate_on_submit():
        data = form.data
        auth = Auth(
            name=data["name"],
            url=data["url"]
        )
        db.session.add(auth)
        db.session.commit()
        flash("添加权限成功！", "okey")
    return render_template('admin/addAuth.html', form=authForm)


# 权限列表
@admin.route('/admin/auth/list/<int:page>', methods=['get'])
@adminLoginRule
def authList(page=None):
    if page == None:
        page = 1
    pageData = Auth.query.order_by(
        Auth.addTime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/authList.html', pageData=pageData)


@admin.route('/admin/auth/del/<int:id>', methods=['get', 'post'])
@adminLoginRule
def delAuth(id=None):
    auth = Auth.query.filter_by(
        id=id
    ).first_or_404()
    db.session.delete(auth)
    db.session.commit()
    flash("删除权限成功！", "okey")
    return redirect(url_for("admin.authList", page=1))


# 添加角色
@admin.route('/admin/role/add/', methods=['get', 'post'])
@adminLoginRule
def addRole():
    roleForm = RoleForm()
    if roleForm.validate_on_submit():
        data = roleForm.data
        role = Role(
            name=data["name"],
            auth=",".join(map(lambda v: str(v), data["auth"]))
        )
        db.session.add(role)
        db.session.commit()

        flash("添加角色成功！", "okey")
    return render_template("admin/addRole.html", form=roleForm)


# 角色列表
@admin.route('/admin/role/list/<int:page>', methods=['get'])
@adminLoginRule
def roleList(page=None):
    if page == None:
        page = 1
    pageData = Role.query.order_by(
        Role.addTime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/roleList.html', pageData=pageData)


# 添加管理员
@admin.route("/admin/add/", methods=["GET", "POST"])
@adminLoginRule
def addAdmin():
    adminform = AdminForm()
    from werkzeug.security import generate_password_hash
    if adminform.validate_on_submit():
        data = adminform.data
        admin = Admin(
            account=data["account"],
            pwd=generate_password_hash("pwd"),
            role_id=data["role_id"],
            is_super=1
        )
        db.session.add(admin)
        db.session.commit()
        flash("添加管理员成功！", "okey")
    return render_template("admin/addAdmin.html", form=adminform)


# 管理员列表
@admin.route('/admin/list/<int:page>', methods=['get', 'post'])
@adminLoginRule
def adminList(page=None):
    if page == None:
        page = 1
    pageData = Admin.query.join(
        Role
    ).filter(
        Role.id == Admin.role_id
    ).order_by(
        Admin.addTime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/adminList.html', pageData=pageData)


@admin.route('/admin/del/<int:id>', methods=['get', 'post'])
@adminLoginRule
def delAdmin(id=None):
    admin = Admin.query.filter_by(
        id=id
    ).first_or_404()
    db.session.delete(admin)
    db.session.commit()
    flash("删除管理员成功！", "okey")
    return redirect(url_for("admin.adminList", page=1))


@admin.route('/admin/update/', methods=['get', 'post'])
@adminLoginRule
def updatePics(id=1):
    linkForm = LinkForm()
    if linkForm.validate_on_submit():
        link = Link.query.get_or_404(id)
        print(link)
        data = linkForm.data
        link.first = data['first'],
        link.second = data['second'],
        link.third = data['third'],
        link.forth = data['forth'],
        link.fifth = data['fifth']
        db.session.add(link)
        db.session.commit()
        flash('更新成功！', 'okey')
        return redirect(url_for('admin.updatePics'))
    return render_template('admin/updatePics.html', form=linkForm)


# 留言列表
@admin.route('/admin/msg/list/<int:page>', methods=['get'])
@adminLoginRule
def msgList(page=None):
    if page == None:
        page = 1
    pageData = Message.query.order_by(
        Message.addTime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/msgList.html', pageData=pageData)


@admin.route('/admin/msg/del/<int:id>', methods=['get', 'post'])
@adminLoginRule
def delMsg(id=None):
    msg = Message.query.filter_by(
        id=id
    ).first_or_404()
    db.session.delete(msg)
    db.session.commit()
    flash("删除留言成功！", "okey")
    return redirect(url_for("admin.msgList", page=1))


@admin.route('/admin/comment/list/<int:page>', methods=['get'])
@adminLoginRule
def commentList(page=None):
    if page == None:
        page = 1
    pageData = Comment.query.join(
        User
    ).join(
        Article
    ).filter(
        Comment.user_id == User.id,
        Comment.article_id == Article.id
    ).order_by(
        Comment.addTime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/commentList.html', pageData=pageData)


# Add news category
@admin.route("/admin/news/cate/add/", methods=["GET", "POST"])
@adminLoginRule
def add_news_cate():
    news_cate_form = NewsCateForm()
    if news_cate_form.validate_on_submit():
        data = news_cate_form.data
        newsCateCount = NewsCate.query.filter_by(news_cate_name=data['name']).count()
        if newsCateCount >= 1:
            flash('新闻分类已经存在！', 'error')
            return redirect(url_for('admin.add_news_cate'))
        news_cate = NewsCate(
            news_cate_name=data["name"],
        )
        db.session.add(news_cate)
        db.session.commit()
        flash("添加新闻分类成功！", "okey")
        redirect(url_for("admin.add_news_cate"))
    return render_template("admin/addNewsCate.html", form=news_cate_form)


@admin.route("/admin/news/cate/list/<int:page>", methods=["GET"])
@adminLoginRule
def news_cate_list(page):
    if page == None:
        page = 1
    pageData = NewsCate.query.order_by(
        NewsCate.addTime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/newsCateList.html", pageData=pageData)


# Add news
@admin.route("/admin/news/add/", methods=["GET", "POST"])
@adminLoginRule
def add_news():
    news_form = NewsForm()
    if news_form.validate_on_submit():
        data = news_form.data
        news_count = News.query.filter_by(title=data['title']).count()
        if news_count >= 1:
            flash('此条资讯已经存在！', 'error')
            return redirect(url_for('admin.add_news'))
        else:
            news = News(
                cate_id=data['newsCateId'],
                title=data['title'],
                content=data['content'],
                source=data['source'],
                copyrightNotice=data['copyrightNotice'],
                publisher=data['publisher']
            )
        db.session.add(news)
        db.session.commit()
        flash("添加资讯成功！", "okey")
        redirect(url_for("admin.add_news"))
    return render_template("admin/addNews.html", form=news_form)


@admin.route("/admin/news/list/<int:page>", methods=["GET"])
@adminLoginRule
def news_list(page):
    if page == None:
        page = 1
    pageData = News.query.join(
        NewsCate
    ).filter(
        News.cate_id == NewsCate.id
    ).order_by(
        News.addTime.desc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/newsList.html", pageData=pageData)
