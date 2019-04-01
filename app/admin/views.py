from . import admin
from app.admin.forms import LoginForm
from app.models import Admin
from flask import render_template, flash, redirect, url_for, session, request
from functools import wraps


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


@admin.route('/admin/', methods=['get', 'post'])
@adminLoginRule
def index():
    return render_template('admin/index.html')



