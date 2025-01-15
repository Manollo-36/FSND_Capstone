
import os
import unittest
import json
from flaskr import create_app
from models import db

database_path = os.environ['DATABASE_URL']

no_token_jwt = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer'
    }

Assistant_jwt = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {TOKEN}'
    }
Director_jwt = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {TOKEN}'
    }
Producer_jwt = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {TOKEN}'
    }


class TriviaTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        # self.database_name = "trivia_test"
        # self.database_user = "Emmanuel"
        # self.database_password = "Manos"
        # self.database_host = "localhost:5432"
        self.database_path = database_path #f"postgresql://{self.database_user}:{self.database_password}@{self.database_host}/{self.database_name}"

        # Create app with the test configuration
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "TESTING": True
        })
        self.client = self.app.test_client

        # Bind the app to the current context and create all tables
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            db.session.remove()
            #db.drop_all()
            
    # test to get all movies by Assistant role
    def test_get_movies(self):
        res = self.client().get('/movies', headers=Assistant_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['Movies'])
    
    # test to get all movies with no token
    def test_get_movies_unauthorized(self):
        res = self.client().get('/movies', headers=no_token_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["code"], 'invalid_header')
        self.assertEqual(data["description"], "Token not found.")  


    # test to get all actors by Casting Director role
    def test_get_actors(self):
        res = self.client().get('/actors', headers=Director_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['Movies'])

    # test to get all actors with no token
    def test_get_actors_unauthorized(self):
        res = self.client().get('/actors',headers=no_token_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["code"], 'invalid_header')
        self.assertEqual(data["description"], "Token not found.")  


    # test to add (post) actor by Executive Producer role
    def test_add_actor(self):
        res = self.client().post('/actors', headers=Producer_jwt,json={"movie_ids":[1], "full_name":"Robert Downey Jr.","age":45,"gender":"Male"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['Actor'])

    # test to add (post) actor by Director role
    def test_add_actor_unauthorized(self):
        res = self.client().post('/actors', headers=Director_jwt,json={"movie_ids":[1], "full_name":"Robert Downey Jr.","age":45,"gender":"Male"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["code"], 'unauthorized')
        self.assertEqual(data["description"], "Permission not found.")
  
    # test to add (post) movie by Executive Producer role
    def test_add_movie(self):
        res = self.client().post('/movies', headers=Producer_jwt,json={"actor_ids":[1], "title":"Avengers","release_date":"05-04-2012","duration":"2,2 hours","imdb_rating":8})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)        
        self.assertIsNotNone(data['Movie'])

    # test to add (post) movie by Assistant role
    def test_add_movie_unauthorized(self):
        res = self.client().post('/movies', headers=Assistant_jwt,json={"actor_ids":[1], "title":"Avengers","release_date":"05-04-2012","duration":"2,2 hours","imdb_rating":8})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["code"], 'unauthorized')
        self.assertEqual(data["description"], "Permission not found.")

    # test to update (patch) movie by Executive Producer role
    def test_update_movie(self):
        res = self.client().patch('/movies/1', headers=Producer_jwt,json={"imdb_rating":9})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)        
        self.assertIsNotNone(data['Movie'])

    # test to add (patch) movie by Assistant role
    def test_update_movie_unauthorized(self):
        res = self.client().post('/movies/1', headers=Assistant_jwt,json={"imdb_rating":9})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["code"], 'unauthorized')
        self.assertEqual(data["description"], "Permission not found.")
    
    # test to delete (delete) movie by Executive Producer role
    def test_delete_movie(self):
        res = self.client().patch('/movies/1', headers=Producer_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)        
        self.assertIsNotNone(data['Movie'])

    # test to delete (delete) movie by Assistant role
    def test_delete_movie_unauthorized(self):
        res = self.client().post('/movies/1', headers=Assistant_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["code"], 'unauthorized')
        self.assertEqual(data["description"], "Permission not found.")


if __name__ == "__main__":
    unittest.main()