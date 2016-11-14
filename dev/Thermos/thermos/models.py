from datetime import datetime
from sqlalchemy import desc
from flask_login import UserMixin
from thermos import db


class Bookmark(db.Model):
    id_boormark = db.Column(db.Integer, primary_key=True)
    nm_url = db.Column(db.Text, nullable=False)
    dt_bookmark = db.Column(db.DateTime, default=datetime.utcnow)
    nm_description = db.Column(db.String(300))
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=False)

    @staticmethod
    def newest(num):
        return Bookmark.query.order_by(desc(Bookmark.dt_bookmark)).limit(num)


    def __repr__(self):
        return "<Bookmark '{}': '{}'>".format(self.nm_description, self.nm_url)


class User(db.Model, UserMixin):
    id_user = db.Column(db.Integer, primary_key=True)
    nm_firstName = db.Column(db.String(120), nullable=False)
    nm_lastName = db.Column(db.String(120), nullable=False)
    nm_userName = db.Column(db.String(80), unique=True)
    nm_email = db.Column(db.String(120), unique=True)
    bookmarks = db.relationship('Bookmark', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.nm_userName
