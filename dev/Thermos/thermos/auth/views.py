from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user

from . import auth
from .. import db
from .. models import User
from . forms import LoginForm, SingupForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #Login and validate user...
        username = form.nm_userName.data
        password = form.nm_password.data
        user = User.get_by_username(username)   
        if user is not None and user.check_password(password):
            login_user(user, form.remember_me.data)            
            flash('Logged in successfully as {0}.'.format(username))
            return redirect(request.args.get('next') or url_for('user', username=username))
        flash('Incorrect username or password.')
    return render_template('login.html', form=form)


@auth.route('/singup', methods=['GET', 'POST'])
def singup():
    form = SingupForm()
    if form.validate_on_submit():
        firstname = form.nm_firstName.data
        lastname = form.nm_lastName.data
        email = form.nm_email.data
        username = form.nm_userName.data
        password = form.nm_password.data
        user = User(nm_firstName=firstname, 
                    nm_lastName=lastname, 
                    nm_email=email, 
                    nm_userName=username, 
                    password=password)
        db.session.add(user)
        db.session.commit()
        flash('Welcome, {0}! Please login'.format(firstname))
        return redirect(url_for('login'))
    return render_template('singup.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))    