from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, login_user, logout_user, current_user

from thermos import app, db, login_manager
from . forms import BookmarkForm, LoginForm, SingupForm
from . models import User, Bookmark, Tag

@login_manager.user_loader
def logged_in_user(userid):
    return User.get_by_id(int(userid))


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           new_bookmarks=Bookmark.newest(5))


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_bookmark():
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.nm_url.data
        description = form.nm_description.data
        tags = form.tags.data
        bm = Bookmark( user=current_user, nm_url=url, nm_description=description, tags=tags)
        db.session.add(bm)
        db.session.commit()
        flash('Stored url: {0} - {1}'.format(url, description))
        return redirect(url_for('user', username=bm.user.nm_userName))
    return render_template('bookmark_form.html', form=form, title='Add a New Bookmark', titleHeader='Add a URL new link')
    '''WORKING WHITHOU WTF
        if request.method == "POST":
            url = request.form['url']
            description = request.form['description']
            store_bookmark(url, description)
            flash('Stored url: {0} - {1}'.format(url, description))
            return redirect(url_for('add'))
        return render_template('bookmark_form.html')
    '''

@app.route('/edit/<int:bookmarkid>', methods=['GET', 'POST'])
@login_required
def edit_bookmark(bookmarkid):
    bm = Bookmark.query.get_or_404(bookmarkid)
    if(current_user != bm.user):
        abort(403)
    form = BookmarkForm(obj=bm)
    if form.validate_on_submit():
        form.populate_obj(bm)
        db.session.commit()
        flash('Stored url: {0} - {1}'.format(url, description))
        return redirect(url_for('user', username=current_user.nm_userName))
    return render_template('bookmark_form.html', form=form, title='Edit Bookmark', titleHeader='Edit Bookmark')

@app.route('/login', methods=['GET', 'POST'])
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


@app.route('/singup', methods=['GET', 'POST'])
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


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))    


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.get_by_username(username,True)
    return render_template('user.html', user=user)

@app.route('/tag/<name>')
def tag(name):
    tag = Tag.get_by_name(name, True)
    return render_template('tag.html', tag=tag)

@app.errorhandler(401)
def unauthorized(e):
    return render_template('401.html'), 401

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

@app.context_processor
def inject_tags():
    return dict(all_tags=Tag.all)    
