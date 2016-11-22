from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from . import bookmark
from thermos import db
from . forms import BookmarkForm
from .. models import Bookmark, Tag



@bookmark.route('/add', methods=['GET', 'POST'])
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
        return redirect(url_for('auth.user', username=bm.user.nm_userName))
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

@bookmark.route('/edit/<int:bookmarkid>', methods=['GET', 'POST'])
@login_required
def edit_bookmark(bookmarkid):
    bm = Bookmark.query.get_or_404(bookmarkid)
    if(current_user != bm.user):
        abort(403)
    form = BookmarkForm(obj=bm)
    if form.validate_on_submit():
        form.populate_obj(bm)
        db.session.commit()
        flash('Stored url: {0} - {1}'.format(bm.nm_url, bm.nm_description))
        return redirect(url_for('auth.user', username=current_user.nm_userName))
    return render_template('bookmark_form.html', form=form, title='Edit Bookmark', titleHeader='Edit Bookmark')


@bookmark.route('/delete/<int:bookmarkid>', methods=['GET', 'POST'])
@login_required
def delete_bookmark(bookmarkid):
    bm = Bookmark.query.get_or_404(bookmarkid)
    if(current_user != bm.user):
        abort(403)
    if request.method == "POST":
        db.session.delete(bm)
        db.session.commit()
        flash("Deleted {}".format(bm.nm_description))
        return redirect(url_for('auth.user', username=current_user.nm_userName))
    else:
        flash("Please confirm deleting the bookmark.")
    return render_template('confirm_delete.html', bm=bm, nolinks=True)

@bookmark.route('/tag/<name>')
def tag(name):
    tag = Tag.get_by_name(name, True)
    return render_template('tag.html', tag=tag)
