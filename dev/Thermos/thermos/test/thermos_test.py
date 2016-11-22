from flask import url_for
from flask.ext.testing import TestCase

import thermos
from thermos.models import User, Bookmark

class ThermosTestCase(TestCase):
    def create_app(self):
        return thermos.create_app('test')

    def setUp(self):
        self.db = thermos.db
        self.db.create_all()
        self.client = self.app.test_client()

        password = 'pbkdf2:sha1:1000$KTWMA2qC$6675e6362c9ba12c3d483ede406061272b900368'
        u = User(nm_firstName='Camila', nm_lastName='Serrão', nm_userName='milla51', 
                nm_email='milla51.serrao@gmail.com', nm_passwordHash=password)
        bm = Bookmark(user=u, nm_url='http://example.com', nm_description='Just an example', tags='one,two,three')

        self.db.session.add(u)
        self.db.session.add(bm)
        self.db.session.commit()

        self.client.post(url_for('auth.login'), 
                        data=dict(nm_userName='milla51', password='123'))

    def tearDown(self):
        thermos.db.session.remove()
        thermos.db.drop_all()
    
    def test_delete_all_tags(self):
        response = self.client.post(
            url_for('bookmark.edit_bookmark', bookmarkid=2),
            data=dict(
                url='http://teste.example.com',
                tags=''
            ),
            follow_redirects = True
        )

        assert response.status_code == 200
        bm = Bookmark.query.get(2)
        assert not bm._tags

