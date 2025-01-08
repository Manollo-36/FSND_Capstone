
import os
from sqlalchemy import Column, String,Integer,DateTime
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
    db.create_all()


class Actor(db.Model):
    __tablename__ = 'actor'
    id = Column(Integer, primary_key=True)
    full_name = Column(String,nullable=False)
    age = Column(Integer,nullable=False)
    gender = Column(String,nullable=False)

 
    def __init__(self, full_name, age,gender):
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



class Movies(db.Model):  
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    actor_id= db.Column(db.Integer,db.ForeignKey('actor.id'),nullable=False)  
    title = Column(String,nullable=False)
    release_date = Column(DateTime,nullable=True)
    duration = Column(Integer, nullable=False)
    imdb_rating = Column(Integer, nullable=False)
    cast = db.relationship('Actor',backref='movies', lazy='joined',cascade='all,delete')

    def __init__(self, title, release_date,duration,imdb_rating,cast):
        self.title = title
        self.release_date = release_date
        self.duration =duration
        self.imdb_rating =imdb_rating
        self.cast =cast

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date}    
        
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