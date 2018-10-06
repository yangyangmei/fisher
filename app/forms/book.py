"""
    created by yangyang on 2018/9/29.
"""
from wtforms import Form, StringField, validators, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired, Regexp

__author__ = "yangyang"


class SearchForm(Form):
    q = StringField(validators=[DataRequired(),Length(min=1,max=30)])
    page = IntegerField(validators=[NumberRange(min=1,max=99)], default=1)

class DriftForm(Form):
    recipient_name = StringField("收件人姓名",validators=[DataRequired()])
    mobile = StringField("手机号", validators=[DataRequired(), Regexp("^1[0-9]{10}$", 0 ,"请输入正确的手机号")])
    message= StringField("留言")
    address = StringField("邮寄地址", validators=[DataRequired(), Length(min=10, max=70, message="地址尽量写详细")])