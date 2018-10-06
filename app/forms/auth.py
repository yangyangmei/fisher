"""
    created by yangyang on 2018/10/1.
"""
from wtforms import Form,StringField,PasswordField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo

from app.models.user import User

__author__ = "yangyang"

class EmailForm(Form):
    email = StringField(validators=[DataRequired(), Email(message="电子邮箱不符合规范"), Length(8, 64)])

class LoginForm(EmailForm):
    # email = StringField(validators=[DataRequired(), Email(message="电子邮箱不符合规范"), Length(8, 64)])
    password = PasswordField(validators=[DataRequired(message="密码不可以为空，请求输入你的密码"), Length(6, 32)])


class RegisterForm(LoginForm):
    # email = StringField( validators=[DataRequired(), Email(message="电子邮箱不符合规范"),Length(8,64)])
    nickname = StringField(validators=[DataRequired(), Length(2,10, message="昵称至少需要两个字符，最多10个字符")])
    # password = PasswordField(validators=[DataRequired(message="密码不可以为空，请求输入你的密码"),Length(6,32) ])


    def validate_email( self,field ):
       if  User.query.filter_by(email=field.data).first():
            raise ValidationError("邮箱已被注册")

    def validate_nickname( self, field ):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError("昵称已存在")


class PasswordForm(Form):
    password1 = PasswordField(validators=[
                             DataRequired(), Length(6, 32, message="密码长度至少需要在6-20个字符之间"),
                              EqualTo("password2",message="两次输入的密码不一致")])

    password2 = PasswordField(validators=[DataRequired(), Length(6,32)])
