# coding:utf8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    account = StringField(
        label='账号',
        validators=[
            DataRequired(),
        ],
        render_kw={
            'class': 'form-control',
            'autofocus': 'autofocus',
            'placeholder': '请输入账号',
            'required': 'required'
        }
    )
    pwd = PasswordField(
        label='密码',
        validators=[
            DataRequired(),
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入密码',
            'placeholder': '请输入密码',
        }
    )
    submit = SubmitField(
        '登录',
        render_kw={
            'class': 'btn btn-log btn-primary btn-block'
        }
    )
