import os
from sqlalchemy import Column, String, Integer, DateTime, Date, Table, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from datetime import date
import json
from flask_migrate import Migrate, MigrateCommand

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

def migrate_db(app):
    migrate = Migrate(app, db)
    return migrate

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple versions of a database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


actor_movie = Table('actor_movie', db.Model.metadata,
    Column('actor_id', Integer().with_variant(Integer, "sqlite"), ForeignKey('actor.id'), primary_key=True),
    Column('movie_id', Integer().with_variant(Integer, "sqlite"), ForeignKey('movie.id'), primary_key=True)
) 


class Movie(db.Model):
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    title = Column(String)
    release_date = Column(Date)
    genre = Column(String)
    actors = db.relationship('Actor', secondary=actor_movie, backref=db.backref('movies', lazy='select'))
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'genre': self.genre,
            'release_date': self.release_date.strftime("%Y-%m-%d")
        }

class Actor(db.Model):
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    gender = Column(String)
    birth_date = Column(Date)
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    def format(self):
        return {
            'id': self.id,
            'name': f'{self.first_name} {self.last_name}',
            'age': calculate_age(self.birth_date)
        }


def calculate_age(birth_date):
    today = date.today()
    return (today.year - birth_date.year -
            ((today.month, today.day) < (birth_date.month, birth_date.day)))
            