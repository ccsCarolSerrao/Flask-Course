from thermos import app, db
from thermos.models import User, Bookmark, Tag
from flask.ext.script import Manager, prompt_bool
from flask.ext.migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def insert_data():
    db.create_all()
    password = 'pbkdf2:sha1:1000$KTWMA2qC$6675e6362c9ba12c3d483ede406061272b900368'
    user1 = User(nm_firstName='Carolina', nm_lastName='Serrao', nm_userName='cserrao', nm_email='ccs.serrao@gmail.com', nm_passwordHash=password)
    db.session.add(user1)

    def add_bookmark(url, description, tags):
        db.session.add(Bookmark(nm_url=url, nm_description=description, tags=tags))
    
    for t in ['python', 'webdev', 'programming', 'training', 'news', 'orm', 'databases', 'emacs', 'gtd', 'django']:
        db.session.add(Tag(nm_tag=t))

    db.session.commit()

    add_bookmark('http://www.python.org', 'Python - My favorite language', 'python, programming')
    add_bookmark('http://www.flask.pocoo.org', 'Web development one drop at time.', 'python, programming')
    
    
    
    db.session.add(User(nm_firstName='Marcelli', nm_lastName='Mattos', nm_userName='mmattos', nm_email='mattos,marcelli@gmail.com', nm_passwordHash=password))

    db.session.commit()

    print('Initialized the database')


@manager.command
def dropdb():
    if(prompt_bool("Are you sure you want to lose all your data?")):
        db.reflect()
        db.drop_all()
        print('Dropped the database')


if __name__ == '__main__': 
    manager.run()           