#import os
from flask import Flask,jsonify,request
from flask_cors import CORS
#import json
from models import setup_db, Actor,Movie
from Authentication.auth import AuthError, requires_auth

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/actor',methods=['GET'])
    #@requires_auth('get:Actors')
    def get_actors():
      try:
        actors = Actor.query.order_by(Actor.id).all()
        print (f"actors: {actors}")
        formated_actors= [actor.format() for actor in actors]
        print (f'formated_actors:{formated_actors}')    
        if len(formated_actors) ==0:
            return not_found(404)
        else:
            return jsonify({ "success": True, "actors": formated_actors})
      except Exception as ex:
        print(ex)
      return unprocessable(422)

    @app.route('/movies',methods=['GET'])
    @requires_auth('get:Movies')
    def get_movies():
      try:
        movies = Movie.query.order_by(Movie.id).all()
        print (f"movies: {movies}")
        formated_movies= [movie.format() for movie in movies]
        print (f'formated_actors:{formated_movies}')    
        if len(formated_movies) ==0:
            return not_found(404)
        else:
            return jsonify({ "success": True, "movies": formated_movies})
      except Exception as ex:
        print(ex)
      return unprocessable(422)
    

    @app.route('/actors/and/movies',methods=['POST'])
    #@requires_auth('post:ActorsandMovies')
    def create_actor():  
        body = request.get_json()
        
        #Movie
        title = body["title"]
        release_date = body["release_date"]
        duration = body["duration"]
        imdb_rating = body["imdb_rating"] 
       
        #Actor
        full_name = body["full_name"]
        age = body["age"]
        gender = body["gender"]
       
        try:
            if full_name =='' or age is None or gender is None:
                return bad_request(400)
            
            elif title == "" or release_date is None or  duration is None or imdb_rating is None :
                return bad_request(400)
            else:               
                new_movie = Movie(
                    title =title,
                    release_date =release_date,
                    duration= duration,
                    imdb_rating = imdb_rating
                    #cast =cast
                )
                new_movie.insert() 
                               
                new_actor = Actor(
                        movie_id = new_movie.id,
                        full_name = full_name,
                        age = age,
                        gender = gender 
    
                        #recipe= json.dumps(new_recipe)
                    )
                new_actor.insert()

                response = { "success": True,"New_Actor":new_actor.id, "Actor": [new_actor.format()],"New Movie":new_movie.id, "Movie":[new_movie.format()]}
                return jsonify(response)
        except Exception as ex:
            print(ex)
            return unprocessable(422)
        
    # @app.route('/movies',methods=['POST'])
    # #@requires_auth('post:ActorsandMovies')
    # def create_movies():  
    #     body = request.get_json()
       
    #     #Movie
    #     title = body["title"]
    #     release_date = body["release_date"]
    #     duration = body["duration"]
    #     imdb_rating = body["imdb_rating"] 
    #     cast = body["cast"]
       
    #     try:
            
    #         if title == "" or release_date is None or  duration is None or imdb_rating is None or cast is None:
    #             return bad_request(400)
    #         else:               
    #             new_movie = Movie(
    #                 title =title,
    #                 release_date =release_date,
    #                 duration= duration,
    #                 imdb_rating = imdb_rating,
    #                 cast =cast
    #             )
    #             new_movie.insert() 

    #             response = { "success": True,"New Movie":new_movie.id, "Movie":[new_movie.format()]}
    #             return jsonify(response)
    #     except Exception as ex:
    #         print(ex)
    #         return unprocessable(422)

   
        
    @app.route('/Actor/<int:actor_id>/and/Movie/<int:movie_id>',methods=['PATCH'])
    @requires_auth('patch:ActorAndMovie')
    def update_drinks(self,actor_id,movie_id):  
        body = request.get_json()
        new_full_name = body.get("full_name", None)
        new_age = body.get("age", None)
        new_gender = body.get("gender", None)

        new_title =body.get("title", None)
        new_release_date =body.get("release_date", None)
        new_duration= body.get("duration", None)
        new_imdb_rating = body.get("imdb_rating", None)
        # new_title = new_drink_request["title"]
        # new_recipe = new_drink_request["recipe"]

        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            movies = Movie.query.filter(Movie.id == movie_id).one_or_none()

            if actor is None or movies is None:               
                    return not_found(404)
            else:
                actor.full_name = new_full_name
                actor.age = new_age
                actor.gender = new_gender 
                
                actor.update()

                movies.title = new_title
                movies.release_date = new_release_date
                movies.duration = new_duration
                movies.imdb_rating = new_imdb_rating

                movies.update()
                
                return jsonify({ "success": True, "actor": [actor.format()]})
        except Exception as ex:
            print(ex)
            return unprocessable(422)



    @app.route('/actor/<int:actor_id>/and/movies/<int:movie_id>',methods=['DELETE'])
    @requires_auth('delete:drinks')
    def delete_actor_movie(self,actor_id,movie_id):
        try:
            #print (f"drink_id: {drink_id}")
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            movies = Movie.query.filter(Movie.id == movie_id).one_or_none()
            #print(f"drink: {drink}")
            if actor is None or movies is None:
                return not_found(404)
            else: 
                actor.delete()
                movies.delete()
                return jsonify({"success": True, "deleted": actor_id,"Movie":movie_id})
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
    app.run(host='0.0.0.0', debug=True)
