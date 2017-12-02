# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

app = Flask(__name__)
# Flask的数据库设置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1:3306/test_flask'
# 查询时会显示原始SQL语句
# app.config['SQLALCHEMY_ECHO'] = True
# 动态追踪修改设置，如未设置只会提示警告
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 关联应用
db = SQLAlchemy(app)


class Group(db.Model):
    # 定义表名:默认表名为类名小写，可以使用　 __tablename__ 指定表名
    __tablename__ = 'groups'
    # id: int primary_key primary_key=True
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    # 一对多关系：添加一个反向引用
    # 与 用户 产生关联关系，代表当前这个 组 下面的所有用户
    # 添加一个反向引用，就是给User添加了一个名为group的属性，可以通过这个属性直接取出对应的角色
    # 参数backref为类User申明新属性的方法 参数lazy决定了什么时候SQLALchemy从数据库中加载数据
    users = db.relationship('User', backref='group', lazy='dynamic')

    def __repr__(self):
        return '<Group: %s %s>' % (self.id, self.name)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(20))
    # 外键关联Table:groups的id字段
    # 添加一个外键，角的这个表的的数据的id
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))

    def __repr__(self):
        return '<User: %s %s %s %s %s>' % (self.id, self.name, self.email, self.password, self.group_id)


@app.route('/')
def index():
    return 'index'


if __name__ == '__main__':
    # 删除所有表
    db.drop_all()
    # 创建
    db.create_all()
    # 添加数据
    g1 = Group(name='super')
    g2 = Group(name='viper')
    db.session.add_all([g1, g2])
    db.session.commit()
    #
    # u1 = User(name='zzz', group_id=g1.id)
    # u2 = User(name='xxx', group_id=g2.id)
    # db.session.add_all([u1, u2])
    # db.session.commit()
    us1 = User(name='wang', email='wang@163.com', password='123456', group_id=g1.id)
    us2 = User(name='zhang', email='zhang@189.com', password='201512', group_id=g2.id)
    us3 = User(name='chen', email='chen@126.com', password='987654', group_id=g2.id)
    us4 = User(name='zhou', email='zhou@163.com', password='456789', group_id=g1.id)
    us5 = User(name='tang', email='tang@itheima.com', password='158104', group_id=g2.id)
    us6 = User(name='wu', email='wu@gmail.com', password='5623514', group_id=g2.id)
    us7 = User(name='qian', email='qian@gmail.com', password='1543567', group_id=g1.id)
    us8 = User(name='liu', email='liu@itheima.com', password='867322', group_id=g1.id)
    us9 = User(name='li', email='li@163.com', password='4526342', group_id=g2.id)
    us10 = User(name='sun', email='sun@163.com', password='235523', group_id=g2.id)
    db.session.add_all([us1, us2, us3, us4, us5, us6, us7, us8, us9, us10])
    db.session.commit()

    """
    查询所有用户数据
    查询有多少个用户
    查询第1个用户
    查询id为4的用户[3种方式]
    User.query.get(4)
    User.query.filter_by(id=4).first()
    User.query.filter(User.id==4).all()
    查询名字结尾字符为g的所有数据[开始/包含]
    查询名字不等于wang的所有数据[2种方式]
    查询名字和邮箱都以 li 开头的所有数据[2种方式]
    查询password是 `123456` 或者 `email` 以 `itheima.com` 结尾的所有数据
    查询id为 [1, 3, 5, 7, 9] 的用户列表
    User.query.filter(User.id.in_([1,3,4,5,9])).all()
    查询name为liu的角色数据
    User.query.filter_by(name='liu').first().group
    查询所有用户数据，并以邮箱排序
    User.query.order_by('email').all()
    每页3个，查询第2页的数据
    User.query.paginate(2, 3, False).items
    """

    """
    get() 主键查询
    filter  模糊查询
    filter_by  精确查询
    all()   查询所有
    order_by()  排序
    first()  第一个
    paginate(page, limit, error)  分页查询数据
    """
    app.run(debug=True, host='0.0.0.0')
