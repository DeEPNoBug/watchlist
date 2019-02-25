#!/usr/bin/python3
# -*- coding: utf-8 -*-


from flask import Flask, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return "hello, world!"


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


if __name__ == '__main__':
    app.run(debug=True)
