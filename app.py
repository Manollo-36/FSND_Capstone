from os import environ as env
#from urllib import response
from flask import Flask,jsonify,request
from flask_cors import CORS
from models import setup_db, Actor,Movie
from Authentication.auth import AuthError, requires_auth
from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = env.get("APP_SECRET_KEY")
    
    with app.app_context():
        setup_db(app)
        CORS(app)       
    
    @app.route('/actors',methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(self):
      try:
        actors = Actor.query.order_by(Actor.id).all()
        print (f"actors: {actors}")
        formated_actors= [actor.format() for actor in actors]
        print (f'formated_actors:{formated_actors}')    
        if len(formated_actors) ==0:
            return not_found(404)
        else:
            return jsonify({ "success": True, "Actors": formated_actors})
      except Exception as ex:
        print(ex)
      return unprocessable(422)

    @app.route('/movies',methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(self):
      try:
        movies = Movie.query.order_by(Movie.id).all()
        print (f"movies: {movies}")
        formated_movies= [movie.format() for movie in movies]
        print (f'formated_actors:{formated_movies}')    
        if len(formated_movies) ==0:
            return not_found(404)
        else:
            return jsonify({ "success": True, "Movies": formated_movies})
      except Exception as ex:
        print(ex)
      return unprocessable(422)
    

    @app.route('/actors',methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(self):  
        body = request.get_json()

        #Actor
        full_name = body.get["full_name"]
        age = body.get["age"]
        gender = body.get["gender"]
        movie_ids = body.get("movie_ids") # List of associated movie IDs
        try:
            if full_name =='' or age is None or gender is None:
                return bad_request(400)
            else:

                new_actor = Actor(
                        full_name = full_name,
                        age = age,
                        gender = gender 
    
                        #recipe= json.dumps(new_recipe)
                    )
                #Associate the actor with movies if movie_ids are provided
                if movie_ids:
                    movies = Movie.query.filter(Movie.id.in_(movie_ids)).all()
                    new_actor.movie_cast.extend(movies)
              
                new_actor.insert()

                response = { "success": True,"New_Actor":new_actor.id, "Actor": [new_actor.format()]}
                return jsonify(response)
        except Exception as ex:
            print(ex)
            return unprocessable(422)
        
    @app.route('/movies',methods=['POST'])
    @requires_auth('post:movies')
    def create_movies(self):  
        body = request.get_json()
       
        #Movie
        title = body.get["title"]
        release_date = body.get["release_date"]
        duration = body.get["duration"]
        imdb_rating = body.get["imdb_rating"] 
        actor_ids = body.get("actor_ids") # List of associated actor IDs
        try:
            
            if title == "" or release_date is None or  duration is None or imdb_rating is None:
                return bad_request(400)
            else: 
                new_movie = Movie(
                    title =title,
                    release_date =release_date,
                    duration= duration,
                    imdb_rating = imdb_rating
                )
                if actor_ids:
                    actors = Actor.query.filter(Actor.id.in_(actor_ids)).all()
                    new_movie.cast.extend(actors)
                new_movie.insert() 

                response = { "success": True,"New Movie":new_movie.id, "Movie":[new_movie.format()]}
                return jsonify(response)
        except Exception as ex:
            print(ex)
            return unprocessable(422)
   
        
    @app.route('/actors/<int:actor_id>',methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(self,actor_id):  
        body = request.get_json()
        new_full_name = body.get("full_name", None)
        new_age = body.get("age", None)
        new_gender = body.get("gender", None)

        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
           
            if actor is None:               
                    return not_found(404)
            else:
                if new_full_name is not None:
                    actor.full_name = new_full_name
                elif new_age is not None:
                    actor.age = new_age
                elif new_gender is not None:
                    actor.gender = new_gender 
                
                actor.update()
                
                return jsonify({ "success": True, "Actor": [actor.format()]})
        except Exception as ex:
            print(ex)
            return unprocessable(422)

    @app.route('/movies/<int:movie_id>',methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(self,movie_id):  
        body = request.get_json()

        new_title =body.get("title", None)
        new_release_date =body.get("release_date", None)
        new_duration= body.get("duration", None)
        new_imdb_rating = body.get("imdb_rating", None)
       
        try:
            movies = Movie.query.filter(Movie.id == movie_id).one_or_none()

            if movies is None:               
                    return not_found(404)
            else:
                if  new_title is not None:  
                    movies.title = new_title
                elif new_release_date is not None:
                    movies.release_date = new_release_date
                elif new_duration is not None:
                    movies.duration = new_duration
                elif new_imdb_rating is not None:    
                    movies.imdb_rating = new_imdb_rating

                movies.update()
                return jsonify({ "success": True, "Movie": [movies.format()]})
        except Exception as ex:
            print(ex)
            return unprocessable(422)


    @app.route('/actors/<int:actor_id>',methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(self,actor_id):
        try:
            #print (f"drink_id: {drink_id}")
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if actor is None:
                return not_found(404)
            else: 
                actor.delete()
                return jsonify({"success": True, "deleted": actor_id,"Actor":actor.format()})
        except Exception as ex:
            print(ex)
            return unprocessable(422)
        
    @app.route('/movies/<int:movie_id>',methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(self,movie_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
           
            if movie is None:
                return not_found(404)
            else: 
                movie.delete()
                return jsonify({"success": True, "deleted": movie_id,"Movie":movie.format()})
        except Exception as ex:
            print(ex)
            return unprocessable(422)
   
# Error Handling
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
            return (
                jsonify(
                    {
                        "success": False,
                        "error": 404,
                        "message": "resource not found",
                    }
                ),
                404,
            )
# @app.errorhandler(405)
# def method_not_allowed(error):
#         return (
#             jsonify(
#                 {
#                     "success": False,
#                     "error": 405,
#                     "message": "method not allowed",
#                 }
#             ),
#             405,
#         )

    @app.errorhandler(400)
    def bad_request(error):
            return (
                jsonify({"success": False, "error": 400, "message": "bad request"}),
                400,
            )

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response =  jsonify({"success":False,"error":ex.status_code,"message":ex.error}),ex.status_code
        #response.status_code = ex.status_code
        return response
    return app
  
app = create_app()

if __name__ == '__main__':
    app.run(host="localhost",debug=True,port="8100")
