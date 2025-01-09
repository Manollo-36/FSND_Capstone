
import os
from sqlalchemy import Column, String,Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    print(database_path)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.drop_all()
    db.create_all()

#association_table
actor_movie = db.Table('actor_movie',
    Column('id', db.Integer, primary_key=True),
    Column('movie_id', db.Integer, db.ForeignKey('Movie.id')),
    Column('actor_id', db.Integer, db.ForeignKey('Actor.id'))
)

class Movie(db.Model):  
    __tablename__ = 'Movies'
    id = Column(Integer, primary_key=True)        
    title = Column(String,nullable=False)
    release_date = Column(String,nullable=True)
    duration = Column(String, nullable=False)
    imdb_rating = Column(Integer, nullable=False)
    cast = db.relationship('Actor', secondary=actor_movie,backref=db.backref('movie_cast', lazy=True,cascade='all, delete' ))

    def __init__(self, title, release_date,duration,imdb_rating):
        self.title = title
        self.release_date = release_date
        self.duration =duration
        self.imdb_rating =imdb_rating

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'duration':self.duration,         
            'imdb_rating':self.imdb_rating}    
        
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()  

    def update(self):
        db.session.commit()

class Actor(db.Model):
    __tablename__ = 'Actors'
    id = Column(Integer, primary_key=True)
    full_name = Column(String,nullable=False)
    age = Column(Integer,nullable=False)
    gender = Column(String,nullable=False)   
 
    def __init__(self,full_name, age,gender):
            self.full_name = full_name
            self.age = age
            self.gender = gender

    def format(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'age': self.age,
            'gender':self.gender}
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()  

    def update(self):
        db.session.commit()


def __repr__(self):
    return json.dumps(self.short())