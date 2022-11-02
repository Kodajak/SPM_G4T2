import unittest
import responses
import requests
import sys
sys.path.append('../app.py')
import app

class test_create_Skills(unittest.TestCase):

# Testing functions with API calls
    @responses.activate
    def test_create(self):
        responses.post(
            url = 'http://localhost:5000/create_Skill',
            json = {"data":["skill", "this is the skill description"]},
            status=200
        )
        resp = requests.post("http://localhost:5000/create_Skill", {"data":["skill", "description"]})

if __name__ == '__main__':
    unittest.main()