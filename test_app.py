import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import requests
from database.models import setup_db, Movie, Actor
from config import host_url, executive_producer_headers, casting_director_headers, casting_assistant_headers  
from app import create_app

class CastingAgencyAPITestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        setup_db(self.app)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            # self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_movies(self):
        
        res = requests.get(f'{host_url}/movies',
                           headers=casting_assistant_headers)
        data = res.json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_fail_auth_get_movies(self):
        
        res = requests.get(f'{host_url}/movies')
        data = res.json()

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["description"],
                         "Authorization header is expected.")
        
    def test_fail_get_movies(self):
        res = requests.get(f'{host_url}/movies?page=100',
                           headers=casting_assistant_headers)
        data = res.json()

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
    
    def test_get_movie(self):
        res = requests.get(f'{host_url}/movies/2',
                           headers=casting_assistant_headers)
        data = res.json()
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie']['id'], 2)
    
    def test_fail_get_movie(self):
        res = requests.get(f'{host_url}/movies/1000',
                           headers=casting_assistant_headers)
        data = res.json()
        
        self.assertEqual(res.status_code, 404)

    # def test_post_movies(self):
    #     payload = {
    #         "title": "Cool dRunnings",
    #         "release_date": "1990-9-12",
    #         "genre": "Comedy"
    #     }
    #     res = requests.post(f'{host_url}/movies',
    #                        headers=executive_producer_headers,
    #                        json=payload)
    #     datad = res.json()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(datad['success'])
    def test_fail_auth_post_movies(self):
        payload = {
            "title": "Cool dRunnings",
            "release_date": "1990-9-12",
            "genre": "Comedy"
        }
        res = requests.post(f'{host_url}/movies',
                           headers=casting_director_headers,
                           json=payload)
        data = res.json()
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["description"],
                         "Permission not found.")

    def test_fail_post_movies(self):
        payload = {
            "title": "Cool Runnings",
            "release_date": "1990-9-12"
        }
        res = requests.post(f'{host_url}/movies',
                           headers=executive_producer_headers,
                           json=payload)

        self.assertEqual(res.status_code, 422)
      

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()