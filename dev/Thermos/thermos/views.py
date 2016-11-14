from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user

from thermos import app, db, login_manager
from . forms import BookmarkForm, LoginForm
from . models import User, Bookmark

@login_manager.user_loader
def logged_in_user(userid):
    return User.query.get(int(userid))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           new_bookmarks=Bookmark.newest(5))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        bm = Bookmark(nm_url=url, nm_description=description, user=logged_in_user())
        db.session.add(bm)
        db.session.commit()
        flash('Stored url: {0} - {1}'.format(url, description))
        return redirect(url_for('add'))
    return render_template('add.html', form=form)
    '''WORKING WHITHOU WTF
        if request.method == "POST":
            url = request.form['url']
            description = request.form['description']
            store_bookmark(url, description)
            flash('Stored url: {0} - {1}'.format(url, description))
            return redirect(url_for('add'))
        return render_template('add.html')
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #Login and validate user...
        username = form.username.data
        user = User.query.filter_by(nm_userName=username).first()
        if user is not None:
            login_user(user, form.remember_me.data)            
            flash('Logged in successfully as {0}.'.format(username))
            return redirect(request.args.get('next')) or url_for('index')
        flash('Incorrect username or password.')
    return render_template('login.html', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(nm_userName=username).first_or_404()
    return render_template('user.html', user=user)

@app.errorhandler(401)
def unauthorized(e):
    return render_template('401.html'), 401

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
