from datetime import datetime
from sqlalchemy import desc
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from thermos import db

tags = db.Table('bookmark_tag',
                db.Column('id_tad',db.Integer, db.ForeignKey('tag.id_tag'), nullable=False),
                db.Column('id_bookmark',db.Integer, db.ForeignKey('bookmark.id_bookmark'), nullable=False))


class Bookmark(db.Model):
    id_bookmark = db.Column(db.Integer, primary_key=True)
    nm_url = db.Column(db.Text, nullable=False)
    dt_bookmark = db.Column(db.DateTime, default=datetime.utcnow)
    nm_description = db.Column(db.String(300))
    id_user = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=False)
    _tags = db.relationship('Tag', secondary=tags, backref=db.backref('bookmarks', lazy='dynamic'))

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
    nm_passwordHash = db.Column(db.String)
    nm_email = db.Column(db.String(120), unique=True)
    bookmarks = db.relationship('Bookmark', backref='user', lazy='dynamic')
    
    def get_id(self):
        '''Overrride method from UserMixin'''
        try:
            return self.id_user
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.nm_passwordHash = generate_password_hash(password)
        return
    
    def check_password(self, password):
        return check_password_hash(self.nm_passwordHash, password)
    
    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(nm_userName=username).first_or_404()

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(nm_email=email).first()

    @staticmethod
    def get_by_id(userid):
        return User.query.get(userid)

    def __repr__(self):
        return '<User %r>' % self.nm_userName

class Tag(db.Model):
    id_tag = db.Column(db.Integer, primary_key=True)
    nm_tag = db.Column(db.String(25), nullable=False, unique=True, index=True)

    def __repr__(self):
        return self.nm_tag       
