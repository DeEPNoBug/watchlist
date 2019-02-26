#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys

from flask import Flask
from flask_login import LoginManager, login_manager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
from watchlist import app, db
from watchlist.models import User, Movie

WIN = sys.platform.startswith('win')
if WIN:  # 如果是windows系统，使用三个斜线
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manger = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    from watchlist.models import User
    user = User.query.get(int(user_id))
    return user


login_manager.login_view = 'login'


@app.context_processor
def inject_user():
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)


from watchlist import views, errors, commands
