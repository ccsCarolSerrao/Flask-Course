
from flask import render_template

from .. import login_manager
from . import main
from .. models import User, Bookmark, Tag


@login_manager.user_loader
def logged_in_user(userid):
    return User.get_by_id(int(userid))


@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html',
                           new_bookmarks=Bookmark.newest(5))

@main.app_errorhandler(401)
def unauthorized(e):
    return render_template('401.html'), 401

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

@main.app_context_processor
def inject_tags():
    return dict(all_tags=Tag.all)    
