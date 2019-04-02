# coding:utf8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, FileField
from wtforms.validators import DataRequired
from app.models import Artcate

artcate = Artcate.query.all()


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


class ArtCateForm(FlaskForm):
    name = StringField(
        label='博文分类',
        validators=[
            DataRequired(),
        ],
        render_kw={
            'class': 'form-control',
            'autofocus': 'autofocus',
            'placeholder': '请输入分类',
            'required': 'required'
        }
    )
    submit = SubmitField(
        '添加',
        render_kw={
            'class': 'btn btn-log btn-primary btn-block'
        }
    )


class ArtForm(FlaskForm):
    title = StringField(
        label='博文标题',
        validators=[
            DataRequired(),
        ],
        render_kw={
            'class': 'form-control',
            'autofocus': 'autofocus',
            'placeholder': '请输入标签',
            'required': 'required'
        }
    )
    briefInfo = TextAreaField(
        label="简介",
        validators=[
            DataRequired("请输入简介！")
        ],
        description="简介",
        render_kw={
            "class": "form-control",
            "id": "input_info",
            "rows": 3
        }
    )
    artCateId = SelectField(
        label="分类",
        validators=[
            DataRequired("请选择分类！")
        ],
        coerce=int,
        choices=[(v.id, v.name) for v in artcate],
        description="分类",
        render_kw={
            "class": "form-control"
        }
    )
    cover = FileField(
        label="封面",
        validators=[
            DataRequired("请上传封面！")
        ],
        description="封面"
    )
    submit = SubmitField(
        '发布',
        render_kw={
            'class': 'btn btn-log btn-primary btn-block'
        }
    )
