#! /Envs/Thermos
from thermos import app, db
from thermos.models import User
from flask.ext.script import Manager, prompt_bool

manager = Manager(app)

@manager.command
def initdb():
    db.create_all()
    print('Initialized the database')


@manager.command
def dropdb():
    if(prompt_bool("Are you sure you want to lose all your data?")):
        print('Dropped the database')


if __name__ == '__main__': 
    manager.run()           