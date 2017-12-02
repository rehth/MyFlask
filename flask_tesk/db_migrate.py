# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.debug = True
# Flask的数据库设置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1:3306/test_flask'
# 查询时会显示原始SQL语句
app.config['SQLALCHEMY_ECHO'] = True
# 动态追踪修改设置，如未设置只会提示警告
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 数据库关联
db = SQLAlchemy(app)

# 第一个参数是Flask的实例，第二个参数是Sqlalchemy数据库实例
migrate = Migrate(app, db)

# 管理器关联
manger = Manager(app)
# manager是Flask-Script的实例，这条语句在flask-Script中添加一个db命令
manger.add_command('db', MigrateCommand)


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    users = db.relationship('User', backref='group', lazy='dynamic')
    i = db.Column(db.Integer)

    # repr()方法显示一个可读字符串
    def __repr__(self):
        return '<Group: %s %s>' % (self.id, self.name)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(20))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))


@app.route('/')
def index():
    return 'index'

if __name__ == '__main__':
    manger.run()