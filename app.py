#import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,jsonify,request
from flask_cors import CORS
import json
from models import setup_db, Actor,Movies
from auth import AuthError, requires_auth

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
        movies = Movies.query.order_by(Movies.id).all()
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
    

    @app.route('/Actors/and/Movies',methods=['POST'])
    @requires_auth('post:ActorsandMovies')
    def add_actor_movies(self):  
        body = request.get_json()
        #Actor
        full_name = body["full_name"]
        age = body["age"]
        gender = body["gender"]
        #Movie
        title = body["title"]
        release_date = body["release_date"]
        duration = body["duration"]
        imdb_rating = body["imdb_rating"]        


        try:
            if full_name =='' or age is None or gender is None or title == "" or release_date is None or  duration is None or imdb_rating is None:
                return bad_request(400)
            else: 
                
                new_actor = Actor(
                        full_name = full_name,
                        age = age,
                        gender = gender 
    
                        #recipe= json.dumps(new_recipe)
                    )
                new_actor.insert()

                new_movie = Movies(
                   title =title,
                    release_date =release_date,
                    duration= duration,
                    imdb_rating = imdb_rating
                )
                new_movie.insert()
                
                response = { "success": True, "Actor": [new_actor.format()],"Movie":[new_movie.format()]}
                return jsonify(response)
        except Exception as ex:
            print(ex)
            return unprocessable(422)
        
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

            if actor is None:               
                    return not_found(404)  
            else:
                actor.title = new_title
                #actor.recipe = json.dumps(new_recipe) 
                
                actor.update()
            
                return jsonify({ "success": True, "actor": [actor.format()]})
        except Exception as ex:
            print(ex)
            return unprocessable(422)



    # @app.route('/drinks/<int:drink_id>',methods=['DELETE'])
    # @requires_auth('delete:drinks')
    # def delete_drinks(self,drink_id):
    #     try:
    #         #print (f"drink_id: {drink_id}")
    #         drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    #         #print(f"drink: {drink}")
    #         if drink is None:
    #             return not_found(404)
    #         else: 
    #             drink.delete()
    #             return jsonify({"success": True, "delete": drink_id})
    #     except Exception as ex:
    #         print(ex)
    #         return unprocessable(422)
   
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
