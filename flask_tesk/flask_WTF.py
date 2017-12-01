# -*- coding:utf-8 -*-
from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, InputRequired

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.secret_key = 'word'


class MyForm(FlaskForm):
    # InputRequired: 只要有输入内容就可以，不管内容是什么
    # DataRequired：数据必须为真，假如在IntegerField里面输入0，那么该验证不通过
    username = StringField(label='用户名：', validators=[DataRequired()],
                           render_kw={"placeholder": "请输入用户名"})
    password = PasswordField(label='密码：', validators=[DataRequired(), EqualTo('password')],
                             render_kw={"placeholder": "请输入密码"})
    uPassword = PasswordField(label='确认密码：', validators=[DataRequired()],
                              render_kw={"placeholder": "请输入确认密码"})
    submit = SubmitField('提交')


@app.route('/', methods=['post', 'get'])
def demo1():
    my_form = MyForm()
    if request.method == 'POST':
        if my_form.validate_on_submit():
            username = request.form.get('username')
            password = request.form.get('password')
            print username, password
            flash('success！！！')
        else:
                flash('fail！！！')
    return render_template('test_WTF.html', form=my_form)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
