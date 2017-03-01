# -*- coding:utf-8 -*-

from flask import render_template, flash, redirect, url_for, request
from flask.ext.login import current_user, login_required

from . import home

@home.route('/', methods=['GET'])
@login_required
def index():
    return render_template('home/index.html')