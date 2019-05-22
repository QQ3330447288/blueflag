# coding:utf8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, FileField, SelectMultipleField
from wtforms.validators import DataRequired, EqualTo
from app.models import Cate, Auth, Role

cate = Cate.query.all()
authlst = Auth.query.all()
roleLst = Role.query.all()


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


# 文章表单
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
            "rows": 3,
            "maxlength": "150",
        }
    )
    content = TextAreaField(
        label="内容",
        validators=[
            DataRequired("请输入简介！")
        ],
        description="简介",
        render_kw={
            "class": "form-control",
            "rows": 7,
            'id': 'result',
        }
    )
    artCateId = SelectField(
        label="分类",
        validators=[
            DataRequired("请选择分类！")
        ],
        coerce=int,
        choices=[(v.id, v.name) for v in cate],
        description="分类",
        render_kw={
            "class": "form-control"
        }
    )
    cover = FileField(
        label="封面",
        description="封面"
    )
    submit = SubmitField(
        '发布',
        render_kw={
            'class': 'btn btn-log btn-primary btn-block'
        }
    )


# 权限表单
class AuthForm(FlaskForm):
    name = StringField(
        label="权限名",
        validators=[
            DataRequired("请输入权限名")
        ],
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入权限名",
        }
    )
    url = StringField(
        label="权限地址",
        validators=[
            DataRequired("请输入权限地址")
        ],
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入权限地址"
        }
    )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary"
        }
    )


# 角色表单
class RoleForm(FlaskForm):
    name = StringField(
        label="角色名称",
        validators=[
            DataRequired("请输入角色名")
        ],
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入角色名",
        }
    )
    auth = SelectMultipleField(
        label="操作权限",
        validators=[
            DataRequired("请选择操作权限！")
        ],
        coerce=int,
        choices=[(v.id, v.name) for v in authlst],
        render_kw={
            "class": "form-control",
        }
    )

    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary"
        }
    )


# 管理员表单
class AdminForm(FlaskForm):
    account = StringField(
        label="管理员名称",
        validators=[
            DataRequired("请输入管理员名")
        ],
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入管理员名",
        }
    )
    pwd = PasswordField(
        label="管理员密码",
        validators=[
            DataRequired("请输入管理员密码")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员密码",
        }

    )
    repwd = PasswordField(
        label="重复管理员密码",
        validators=[
            DataRequired("请重复管理员密码！"),
            EqualTo('pwd', message="两次密码不一致")
        ],
        description="重复密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请重复管理员密码！",
        }
    )
    role_id = SelectField(
        label="所属角色",
        coerce=int,
        choices=[(v.id, v.name) for v in roleLst],
        render_kw={
            "class": "form-control",
        }
    )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary"
        }
    )


class LinkForm(FlaskForm):
    first = StringField(
        label="第一张",
        validators=[
            DataRequired("请输入第一张图片链接")
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "第一张图片链接",
        }
    )
    second = StringField(
        label="第一张",
        validators=[
            DataRequired("请输入第一张图片链接")
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "第一张图片链接",
        }
    )
    third = StringField(
        label="第一张",
        validators=[
            DataRequired("请输入第一张图片链接")
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "第一张图片链接",
        }
    )
    forth = StringField(
        label="第一张",
        validators=[
            DataRequired("请输入第一张图片链接")
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "第一张图片链接",
        }
    )
    fifth = StringField(
        label="第一张",
        validators=[
            DataRequired("请输入第一张图片链接")
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "第一张图片链接",
        }
    )
    submit = SubmitField(
        '更新图片',
        render_kw={
            "class": "btn btn-primary"
        }
    )


# # add technology news
# class NewsForm(FlaskForm):
#

# add technology news category
class NewsCateForm(FlaskForm):
    name = StringField(
        label='新闻分类',
        validators=[
            DataRequired(),
        ],
        render_kw={
            'class': 'form-control',
            'autofocus': 'autofocus',
            'placeholder': '请输入新闻分类',
            'required': 'required'
        }
    )
    submit = SubmitField(
    '添加',
    render_kw={
        'class': 'btn btn-log btn-primary btn-block'
    }
)
