#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
flask 配置
http://flask-sqlalchemy.pocoo.org/2.1/config/

flask-sqlalchemy配置
http://flask-sqlalchemy.pocoo.org/2.1/config/
"""
import os
import sys
import click

from flask import Flask, url_for, render_template, request, flash, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

WIN = sys.platform.startswith('win')
if WIN:  # 如果是windows系统，使用三个斜线
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manger = LoginManager(app)


@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop')
def initdb(drop):
    """Initalize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo("Initialized database.")  # 输出提示信息


@app.cli.command()
def forge():
    """Generate fake data"""
    db.create_all()

    # 全局的两个变量移动到这个函数内
    name = "Grey Li"
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'}
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')


@app.context_processor
def inject_user():  # 函数名可以随意修改
    user = User.query.first()
    return dict(user=user)


@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help="The password used to login.")
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo("Updating user...")
        user.username = username
        user.set_password(password)  # 设置密码

    else:
        click.echo("Create user...")
        user = User(username=username, name="Admin")
        user.set_password(password)
        db.session.add(user)

    db.session.commit()  # 提交数据库会话
    click.echo('Done...')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))  # 名字
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份


@app.route('/')
def index():
    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    return render_template('index.html', name=name, movies=movies)


@app.route('/index')
def index2():
    return "<h1>hello, world!</h1><img src='http://helloflask.com/totoro.gif'>"


@app.route('/user_page/<name>')
def user_page(name):
    return "User: %s" % name


@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', name="zhangsan"))
    print(url_for('user_page', name="peter"))
    print(url_for('test_url_for'))
    print(url_for('test_url_for', num=2))
    return "Test page"


@app.route('/login', methods=['GET', 'POST'])
def login():  # 登录
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not username or not password:
            flash('Invalid input')
            return redirect(url_for('login'))

        user = User.query.first()
        # 验证用户名和密码是否一致
        if username == user.username and user.validate_password(password):
            login_user(user)  # 更如用户
            flash('Login sucess')
            return redirect(url_for('index'))

        flash('Invalid username or password')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()  # 登出用户
    flash('Goodbye.')
    return redirect(url_for('index'))  # 重定向回首页


@login_manger.user_loader
def load_user(user_id):
    # 创建用户加载回调函数，接受用户ID作为参数
    user = User.query.get(int(user_id))
    return user


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash("Item deleted.")
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    user = User.query.first()
    return render_template('404.html', user=user), 404


def say_hello(to=None):
    if to:
        return "Hello, %s!" % to
    return "Hello!"


if __name__ == '__main__':
    app.run(debug=True)
    """
    在视图保护层面来说，未登录用户不能执行下面的操作：
    访问编辑页面
    访问设置页面
    执行注销操作
    执行删除操作
    执行添加新条目操作
    """
