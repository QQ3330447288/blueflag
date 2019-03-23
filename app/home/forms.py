from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Regexp, EqualTo
from app.models import User


class RegisterForm(FlaskForm):
    name = StringField(
        label='用户名',
        validators=[
            DataRequired(),
            Regexp('^[a-zA-Z][a-zA-Z0-9_]{4,15}$', message="必须字母开头,5-16字节,允许字母数字下划线!")
        ],
        render_kw={
            'class': 'form-control',
            'autofocus': 'autofocus',
            'placeholder': '请输入用户名',
            'maxLength': '15'
        }
    )
    phone = StringField(
        label='手机号',
        validators=[
            DataRequired(),
            Regexp('1[34578]\\d{9}', message='手机号格式不正确!')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入手机号',
            'maxLength': '11',
            'id': "phone"
        }
    )
    pwd = PasswordField(
        label='密码',
        validators=[
            DataRequired(),
            Regexp('^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,15}$', message='为了账号的安全,密码必须是大小写字母和数字的组合,不能使用特殊字符,长度在6-15之间!')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入密码',
            'maxLength': '15',
            'minLength': '6'
        }
    )
    code = StringField(
        label='验证码',
        validators=[
            DataRequired(),
            Regexp('^[0-9]*$', message='必须是数字！'),
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入4位手机验证码',
            'maxLength': '4',
            'minLength': '4'
        }
    )
    surePwd = PasswordField(
        label='确认密码',
        validators=[
            DataRequired(),
            Regexp('^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,15}$', message='为了账号的安全,密码必须是大小写字母和数字的组合,不能使用特殊字符,长度在6-15之间!'),
            EqualTo('pwd', message='两次密码输入不一致！')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入确认密码!',
            'maxLength': '20',
            'minLength': '6'
        }
    )
    submit = SubmitField(
        '注册',
        render_kw={
            'class': 'btn btn-log btn-primary btn-block'
        }
    )

    def validate_name(self, field):
        name = field.data
        user_count = User.query.filter_by(name=name).count()
        if user_count >= 1:
            raise ValidationError('该用户名已经被占用！')

    def validate_phone(self, field):
        phone = field.data
        user_count = User.query.filter_by(phone=phone).count()
        if user_count >= 1:
            raise ValidationError('该手机号已经被占用！')


class LoginForm(FlaskForm):
    name = StringField(
        label='用户名',
        validators=[
            DataRequired(),
            Regexp('^[a-zA-Z][a-zA-Z0-9_]{4,15}$', message="必须字母开头,5-16字节,允许字母数字下划线!")
        ],
        render_kw={
            'class': 'form-control',
            'autofocus': 'autofocus',
            'placeholder': '请输入用户名',
            'maxLength': '15'
        }
    )
    pwd = PasswordField(
        label='密码',
        validators=[
            DataRequired(),
            Regexp('^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,15}$', message='为了账号的安全,密码必须是大小写字母和数字的组合,不能使用特殊字符,长度在6-15之间!')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入密码',
            'maxLength': '15',
            'minLength': '6'
        }
    )
    submit = SubmitField(
        '注册',
        render_kw={
            'class': 'btn btn-log btn-primary btn-block'
        }
    )

    def validate_name(self, field):
        name = field.data
        user_count = User.query.filter_by(name=name).count()
        if user_count == 0:
            raise ValidationError('该用户还未注册,请注册后再登录！')
