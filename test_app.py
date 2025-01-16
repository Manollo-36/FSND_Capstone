
import os
import unittest
import json
from flaskr import create_app
from models import db

database_path = os.environ['DATABASE_URL']
ASSISTANT_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImZQM29LdEVZRkhYOE84ejljSE16WiJ9.eyJpc3MiOiJodHRwczovL2ZzbmRtYW5vcy5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8Njc4OGQ4NjRhNzNlZmM4NWZmMTk5ODg0IiwiYXVkIjoiQ2Fwc3RvbmUiLCJpYXQiOjE3MzcwMjE2MDIsImV4cCI6MTczNzAyODgwMiwic2NvcGUiOiIiLCJhenAiOiJTemZXRUdXd2RxVldUWWZVeFlzWG1QVHFkUU5hNlZzTSIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.IQbCtNacmG4k_GgxxPkIIdUcMeM6FruaI_cgH7nNksRXHPkD2TRUkLWGvRvEjahKeQMH7m6IizOX4l8s4pg_pFWrVCQJOw1Eorxb2hqDHaPZM_2nlEuCJm5JMuOXQyrpK_sDcjp2rE24sTvDTcsN0elbG061Yw-O473oSZerNiM89fGypBZ9Jxopnt7kzN3cwBbPH9fF4NgQ0P_rIHsr7_Sj03hZfI8BMHbyja3D0qp1mqUzSfuvEiFH0UdtlXSHWSuD35VTIxZ1pnkUuJw8U_XnbeyAaDTK_7emVCmpA9fJzT4UM0xR7m5eLfTXEceWitePZ5-RpObzlcMHGnIErQ"
DIRECTOR_TOKEN ="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImZQM29LdEVZRkhYOE84ejljSE16WiJ9.eyJpc3MiOiJodHRwczovL2ZzbmRtYW5vcy5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjczNzUxNDU5ZDcyNTAzZjJhMGVlMGFjIiwiYXVkIjoiQ2Fwc3RvbmUiLCJpYXQiOjE3MzcwMjE0NTIsImV4cCI6MTczNzAyODY1Miwic2NvcGUiOiIiLCJhenAiOiJTemZXRUdXd2RxVldUWWZVeFlzWG1QVHFkUU5hNlZzTSIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.gl1SMsHz-P2sto3jyC2AgEz4pxOUJfShzi5HPNLQ_HZPqHA__JFAGaApXE_yZiDtKCBqs1r8LLlpwKCwa9sD-zYM5EoG2R3TXUSXOZOszkvlV7sSyad3DPNqGI5FImUVkb1V2O-Re58-vOcO3ySftB4GKAnvOYUNvnx-35Ot1Fbet9HEHNVGdhs_8YKT3IOlfEAQJ2haI7FBepqnxBa_0KY_rcFiuavA75uGH1LZl2IDO2ec44NgFLR1vODVXWmC06iK2rgVOu9MX5GW3_ecU9X2OO1HtY3Pl7GG-LMCzbl5X0J6OAJRdCcJgfpNfXuMnOXIp4LmkDbaucvQDVb9qQ"
PRODUCER_TOKEN ="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImZQM29LdEVZRkhYOE84ejljSE16WiJ9.eyJpc3MiOiJodHRwczovL2ZzbmRtYW5vcy5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjczMzVmNmYwM2FiYzY1MjBlZmMwM2VlIiwiYXVkIjoiQ2Fwc3RvbmUiLCJpYXQiOjE3MzcwMjA5OTcsImV4cCI6MTczNzAyODE5Nywic2NvcGUiOiIiLCJhenAiOiJTemZXRUdXd2RxVldUWWZVeFlzWG1QVHFkUU5hNlZzTSIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.uGkpE9ZD54qNDoKm9IS0-nA-9IkOXCJq0FyH9CJT6nxTc2LlTj-jNnKaK3yg_yYEALpgStfwiXRc5CXVyTGWQHMwcMhaKBJYin7syy9JAryhphoTM04aXouT8W1xTaew44u9QOg9UMIKfT8V3C-MiAMh6baINouy9NGEfcWyGb6Wqb8diiG46nTFFIktQCNTWZEuWSNQsn5IS1AcMlfIh0uTPaeKLzi2k7N6C6usUJt1UBTUppYe63BO7NFtHIzqauMhriQ997hCITDwNNMShGQDA_NDgqE3o6oTfWiVCp4PIEjPQGOoTpdcaJ3qGjlL2mcnAozwLKw7vDrMZWGKfQ"

no_token_jwt = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer'
    }

Assistant_jwt = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {ASSISTANT_TOKEN}'
    }
Director_jwt = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {DIRECTOR_TOKEN}'
    }
Producer_jwt = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {PRODUCER_TOKEN}'
    }


class TriviaTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""     
        self.database_path = database_path 

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