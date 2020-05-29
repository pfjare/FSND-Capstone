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
        res = requests.get(f'{host_url}/movies/5',
                           headers=casting_assistant_headers)
        data = res.json()
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie']['id'], 5)
    
    def test_fail_get_movie(self):
        res = requests.get(f'{host_url}/movies/1000',
                           headers=casting_assistant_headers)
        data = res.json()
        
        self.assertEqual(res.status_code, 404)


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

    def test_post_movies(self):
        payload = {
            "title": "Cool dRunnings",
            "release_date": "1990-9-12",
            "genre": "Comedy"
        }
        res = requests.post(f'{host_url}/movies',
                           headers=executive_producer_headers,
                           json=payload)
        datad = res.json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(datad['success'])

    def test_fail_auth_patch_movies(self):
        payload = {
            "genre": "Action"
        }
        res = requests.patch(f'{host_url}/movies/9',
                           headers=casting_assistant_headers,
                           json=payload)
        data = res.json()
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["description"],
                         "Permission not found.")     
    def test_patch_movies(self):
        payload = {
            "genre": "Action"
        }
        res = requests.patch(f'{host_url}/movies/9',
                           headers=casting_director_headers,
                           json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        
        self.assertTrue(data['success'])    
        self.assertEqual(data["edited"], 9) 
    def test_fail_patch_movies(self):
        payload = {
            "genre": "Action"
        }
        res = requests.patch(f'{host_url}/movies/1111',
                           headers=casting_director_headers,
                           json=payload)
        self.assertEqual(res.status_code, 404)

    def test_fail_delete_movies(self):
        res = requests.delete(f'{host_url}/movies/1111',
                           headers=executive_producer_headers)
        data = res.json()
        self.assertEqual(res.status_code, 404)
    
    def test_fail_auth_delete_movies(self):
        res = requests.delete(f'{host_url}/movies/2',
                           headers=casting_director_headers)
        data = res.json()
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["description"],
                         "Permission not found.")    
    
    def test_delete_movies(self):
        res = requests.delete(f'{host_url}/movies/9',
                           headers=executive_producer_headers)
        data = res.json()
        self.assertEqual(res.status_code, 200) 
        self.assertTrue(data['success'])    
        self.assertEqual(data["deleted"], 9)   
    
    def test_fail_auth_post_actors(self):
        payload = {
            "first_name": "Will",
            "last_name":"Ferrell",
            "gender":"male",
            "birth_date":"1967-7-16"
        }
        res = requests.post(f'{host_url}/actors',
                           headers=casting_assistant_headers,
                           json=payload)
        data = res.json()
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["description"],
                         "Permission not found.")

    def test_fail_post_actors(self):
        payload = {
            "first_name": "Will",
            "last_name":"Ferrell"
        }
        res = requests.post(f'{host_url}/actors',
                           headers=casting_director_headers,
                           json=payload)

        self.assertEqual(res.status_code, 422)

    def test_post_actors(self):
        payload = {
            "first_name": "Will",
            "last_name":"Ferrell",
            "gender":"male",
            "birth_date":"1967-7-16"
        }
        res = requests.post(f'{host_url}/actors',
                           headers=casting_director_headers,
                           json=payload)
        data = res.json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])    

    def test_fail_auth_get_actors(self):
        
        res = requests.get(f'{host_url}/actors')
        data = res.json()

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["description"],
                         "Authorization header is expected.")
        
    def test_fail_get_actors(self):
        res = requests.get(f'{host_url}/actors?page=100',
                           headers=casting_assistant_headers)
        data = res.json()

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
    
    def test_get_actor(self):
        res = requests.get(f'{host_url}/actors/6',
                           headers=casting_assistant_headers)
        data = res.json()
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['id'], 6)
    
    def test_fail_get_actor(self):
        res = requests.get(f'{host_url}/actors/333',
                           headers=casting_assistant_headers)
        data = res.json()
        
        self.assertEqual(res.status_code, 404) 

    def test_fail_auth_patch_actors(self):
        payload = {
            "birth_date":"1967-7-16"
        }
        res = requests.patch(f'{host_url}/actors/6',
                           headers=casting_assistant_headers,
                           json=payload)
        data = res.json()
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["description"],
                         "Permission not found.")     

    def test_fail_patch_actors(self):
        payload = {
            "birth_date":"1967-7-16"
        }
        res = requests.patch(f'{host_url}/actors/1111',
                           headers=casting_director_headers,
                           json=payload)
        self.assertEqual(res.status_code, 404)

    def test_patch_actors(self):
        payload = {
            "birth_date":"1967-7-16"
        }
        res = requests.patch(f'{host_url}/actors/6',
                           headers=casting_director_headers,
                           json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        
        self.assertTrue(data['success'])    
        self.assertEqual(data["edited"], 6) 
    def test_fail_delete_actors(self):
        res = requests.delete(f'{host_url}/actors/1111',
                           headers=executive_producer_headers)
        data = res.json()
        self.assertEqual(res.status_code, 404)
    
    def test_fail_auth_delete_actors(self):
        res = requests.delete(f'{host_url}/actors/12',
                           headers=casting_assistant_headers)
        data = res.json()
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["description"],
                         "Permission not found.")    
    
    def test_delete_actors(self):
        res = requests.delete(f'{host_url}/actors/12',
                           headers=executive_producer_headers)
        data = res.json()
        self.assertEqual(res.status_code, 200) 
        self.assertTrue(data['success'])    
        self.assertEqual(data["deleted"], 12)  
    
    # def test_post_actor_to_movie(self):
    #     res = requests.post(f'{host_url}/movies/6/actors/5',
    #                        headers=casting_director_headers)
    #     datad = res.json()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(datad['success'])

    # def test_fail_auth_post_actor_to_movie(self):
    #     res = requests.post(f'{host_url}/movies/6/actors/5',
    #                        headers=casting_assistant_headers)
    #     data = res.json()
    #     self.assertEqual(res.status_code, 401)
    #     self.assertEqual(data["description"],
    #                      "Permission not found.")

    # def test_fail_post_actor_to_movie(self):
    #     res = requests.post(f'{host_url}/movies/54/actors/1',
    #                        headers=casting_director_headers)

    #     self.assertEqual(res.status_code, 404)      
    

    # def test_fail_auth_delete_actor_from_movie(self):
    #     res = requests.delete(f'{host_url}/movies/6/actors/4',
    #                        headers=casting_assistant_headers)
    #     data = res.json()
    #     self.assertEqual(res.status_code, 401)
    #     self.assertEqual(data["description"],
    #                      "Permission not found.")

    # def test_fail_delete_actor_from_movie(self):
    #     res = requests.delete(f'{host_url}/movies/54/actors/4',
    #                        headers=casting_director_headers)

    #     self.assertEqual(res.status_code, 404)  
    # def test_delete_actor_from_movie(self):
    #     res = requests.delete(f'{host_url}/movies/6/actors/4',
    #                        headers=casting_director_headers)
    #     datad = res.json()

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(datad['success'])    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()