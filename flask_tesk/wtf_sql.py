# -*- coding:utf-8 -*-
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_WTF import FlaskForm
from wtforms import StringField, validators, SubmitField

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
# Flask的数据库设置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1:3306/test_flask'
# 查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True
# 动态追踪修改设置，如未设置只会提示警告
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 关联应用
db = SQLAlchemy(app)

app.secret_key = 'abc'


class Form(FlaskForm):
    """表单"""
    author = StringField(label='作者：', validators=[validators.DataRequired()])
    book = StringField(label='书名：', validators=[validators.DataRequired()])
    submit = SubmitField('提交')


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    books = db.relationship('Book', backref='author', lazy='dynamic')


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))


@app.route('/', methods=['post', 'get'])
def index():
    form = Form()
    if request.method == 'POST':
        if form.validate_on_submit():
            author = request.form.get('author')
            book = request.form.get('book')
            auth = Author.query.filter_by(name=author).first()
            if auth:
                try:
                    # 作者已存在  添加书
                    if not Book.query.filter_by(name=book).first():
                        # 如果书不存在
                        b = Book(name=book, author_id=auth.id)
                        db.session.add(b)
                        db.session.commit()
                    else:
                        return '该书已存在'
                except Exception as e:
                    db.session.rollback()
                    print e
                    return '添加失败'
            else:
                try:
                    # 添加作者
                    a = Author(name=author)
                    db.session.add(a)
                    db.session.commit()
                    # 在添加书
                    b = Book(name=book, author_id=a.id)
                    db.session.add(b)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print e
                    return '添加失败'
        else:
            return '信息不完整'
    data = Author.query.order_by('id').all()
    return render_template('wtf_sql.html', form=form, data=data)


@app.route('/del/book/<int:book_id>')
def delete_book(book_id):
    book = Book.query.filter(Book.id == book_id).first()
    if book:
        try:
            db.session.delete(book)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print e
            return '删除失败'
    else:
        return '该书不存在'
    return redirect(url_for('index'))


@app.route('/del/author/<int:author_id>')
def delete_author(author_id):
    author = Author.query.get(author_id)
    if author:
        try:
            for book in author.books:
                db.session.delete(book)
            db.session.delete(author)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print e
            return '删除失败'
    else:
        return '该作者不存在'
    # 重定向要用redirect
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    # db.drop_all()
    # db.create_all()
    # # 生成数据
    # au1 = Author(name='老王')
    # au2 = Author(name='老尹')
    # au3 = Author(name='老刘')
    # # 把数据提交给用户会话
    # db.session.add_all([au1, au2, au3])
    # # 提交会话
    # db.session.commit()
    # bk1 = Book(name='老王回忆录', author_id=au1.id)
    # bk2 = Book(name='我读书少，你别骗我', author_id=au1.id)
    # bk3 = Book(name='如何才能让自己更骚', author_id=au2.id)
    # bk4 = Book(name='怎样征服美丽少女', author_id=au3.id)
    # bk5 = Book(name='如何征服英俊少男', author_id=au3.id)
    # # 把数据提交给用户会话
    # db.session.add_all([bk1, bk2, bk3, bk4, bk5])
    # # 提交会话
    # db.session.commit()

