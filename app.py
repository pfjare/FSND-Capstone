import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from database.models import db_drop_and_create_all, setup_db, migrate_db, Movie, Actor
from datetime import date
from auth.auth import AuthError, requires_auth
def create_app():
        
    app = Flask(__name__)
    setup_db(app)
    migrate=migrate_db(app)
    
    # Converts date string to date object
    # String format y-m-d Ex: 2002-5-10
    def convert_date(date_str):
        date_str = date_str.split("-")
        return date(int(date_str[0]), int(date_str[1]), int(date_str[2]))

    ## Movies

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies():
        page = request.args.get('page', 1, type=int)

        # Create Pagination object
        # Will cause 404 error if no items on page are found
        movies = Movie.query.paginate(page=page, per_page=5, error_out=True)

        return jsonify({
            "success": True,
            "movies": [movie.format() for movie in movies.items],
            "total_movies": movies.total
        })
    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth('get:movies')
    def get_movie(movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        
        # Get actors assigned to movie
        actors = Actor.query.filter(Actor.movies.any(Movie.id == movie_id)).all()
        # Format movie
        movie_formatted = movie.format()
        # Add list of actors to movie object
        movie_formatted.update({'actors': [actor.id for actor in actors]})
        
        return jsonify({
            "success": True,
            "movie": movie_formatted
        })



    @app.route('/movies', methods=["POST"])
    @requires_auth('post:movies')
    def add_movie():

        data = request.get_json()
        title = data.get('title', None)
        genre = data.get('genre', None)
        release_date = data.get('release_date', None)

        # Request body must contain title, genre, and release_date
        if genre is None or title is None or release_date is None:
            abort(422)

        movie = Movie(title=title, genre=genre,
                    release_date=convert_date(release_date))

        try:
            movie.insert()
        except exc.SQLAlchemyError as error:
            print(error)
            abort(422)
        return jsonify({
            'success': True,
            'created': movie.id
        })

    @app.route('/movies/<int:movie_id>', methods=["PATCH"])
    @requires_auth('patch:movies')
    def update_movie(movie_id):

        data = request.get_json()
        title = data.get('title', None)
        genre = data.get('genre', None)
        release_date = data.get('release_date', None)

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        if genre:
            movie.genre = genre
        if release_date:
            movie.release_date = convert_date(release_date)
        if title:
            movie.title = title

        try:
            movie.update()
        except exc.SQLAlchemyError as error:
            print(error)
            abort(422)
        return jsonify({
            'success': True,
            'edited': movie.id
        })

    # DELETE /movies/:id - Requires delete:movies permission
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        try:
            movie.delete()
        except exc.SQLAlchemyError as error:
            print(error)
            abort(422)

        return jsonify({
            "success": True,
            "deleted": movie.id
        })

    @app.route('/movies/<int:movie_id>/actors/<int:actor_id>', methods=["POST"])
    @requires_auth('patch:movies')
    def add_actor_to_movie(movie_id, actor_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        # Append actor to movie
        if actor is None:
            abort(404)
        movie.actors.append(actor)
        try:
            movie.update()
        except exc.SQLAlchemyError as error:
            print(error)
            abort(422)    
        return jsonify({
            "success": True
        })    

    @app.route('/movies/<int:movie_id>/actors/<int:actor_id>', methods=["DELETE"])
    @requires_auth('patch:movies')
    def remove_actor_from_movie(movie_id, actor_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)
        movie.actors.remove(actor)
        try:
            movie.update()
        except exc.SQLAlchemyError as error:
            print(error)
            abort(422) 
        return jsonify({
            "success": True
        })

    ## Actors

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors():
        page = request.args.get('page', 1, type=int)

        # Create Pagination object
        # Will cause 404 error if no items on page are found
        actors = Actor.query.paginate(page=page, per_page=5, error_out=True)

        return jsonify({
            "success": True,
            "actors": [actor.format() for actor in actors.items],
            "total_actors": actors.total
        })


    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth('get:actors')
    def get_actor(actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)
        
        # Get movies assigned to actor
        movies = Movie.query.filter(Movie.actors.any(Actor.id == actor_id)).all()
        # format movie
        actor_formatted = actor.format()
        # Add list of movies to actor object
        actor_formatted.update({'movies': [movie.id for movie in movies]})
        return jsonify({
            "success": True,
            "actor": actor_formatted
        })



    @app.route('/actors', methods=["POST"])
    @requires_auth('post:actors')
    def add_actor():

        data = request.get_json()
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)
        gender = data.get('gender', None)
        birth_date = data.get('birth_date', None)
      
        # Request body must contain first_name, last_name,
        # gender, and birth_date
        if (last_name is None or first_name is None or
                gender is None or birth_date is None):
            abort(422)

        actor = Actor(last_name=last_name,
                    first_name=first_name,
                    gender=gender,
                    birth_date=convert_date(birth_date))
        
        try:

            actor.insert()
        except exc.SQLAlchemyError as error:
            print(error)
            abort(422)
        return jsonify({
            'success': True,
            'created': actor.id
        })

    @app.route('/actors/<int:actor_id>', methods=["PATCH"])
    @requires_auth('patch:actors')
    def update_actor(actor_id):

        data = request.get_json()
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)
        gender = data.get('gender', None)
        birth_date = data.get('birth_date', None)

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)

        if first_name:
            actor.first_name = first_name
        if last_name:
            actor.last_name = last_name
        if gender:
            actor.gender = gender
        if birth_date:
            actor.birth_date = convert_date(birth_date)

        try:
            actor.update()
        except exc.SQLAlchemyError as error:
            print(error)
            abort(422)
        return jsonify({
            'success': True,
            'edited': actor.id
        })

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)
        try:
            actor.delete()
        except exc.SQLAlchemyError as error:
            print(error)
            abort(422)

        return jsonify({
            "success": True,
            "deleted": actor.id
        })


    # Error Handling


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "Unprocessable Entity"
            }), 422

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "Resource Not Found"
            }), 404
    @app.errorhandler(400)
    def resource_not_found(error):
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "Bad Request"
            }), 400
    #AuthError defined in auth.py
    @app.errorhandler(AuthError)
    def authentication(error):
        return jsonify(error.error), 401
    
    
    return app
