# -*- coding:utf-8 -*-
from . import auth
from .forms import LoginForm

from flask import render_template, redirect, url_for, request, flash, g
from flask_login import login_user, current_user, login_required, logout_user
from foundation.dataservice import account_impl
from foundation.model.login import Login

from app import login_manager

@login_manager.user_loader
def load_user(username):
    uc =  account_impl.get_by_username(username)
    if not uc:
        return None

    return Login(uc.username)


@auth.before_request
def get_current_user():
    if current_user.is_authenticated:
        g.user = current_user



@auth.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate():
            try:
                account = account_impl.get_by_username(form.username.data)
                if account is not None and Login.validate_login(account.password_hash, form.password.data):
                    user_obj = Login(account.username)
                    login_user(user_obj, form.remember.data)

                    return redirect(url_for('home.index'))
            except Exception as ex:
                flash('#ERROR LOGIN:' + ex.message)
                return render_template('auth/index.html', form=form)


    if form.errors:
        flash(form.errors, 'danger')

    return render_template('auth/index.html', form=form)




@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))





