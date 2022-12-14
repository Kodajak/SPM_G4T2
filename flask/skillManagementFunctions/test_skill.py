import pytest
import unittest
import requests
import mysql.connector as mysql

HOST = "database-1.cmqbhk3xoixj.ap-southeast-1.rds.amazonaws.com" # or "domain.com"
# database name, if you want just to connect to MySQL server, leave it empty
DATABASE = "spmDB"
# "is212_example, spmDB"
# this is the user you create
USER = "admin"
# user password
PASSWORD = "spmspmspm"
# connect to MySQL server
db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
print("Connected to:", db_connection.get_server_info())
cursor = db_connection.cursor()

class TestSkill(unittest.TestCase):

    def setUp(self):
        query = "INSERT INTO Skill (skill_id, skill_name, skill_desc, status) VALUES (%s, %s, %s, %s)"
        val = (999999, "Skill to Delete", "Skill to Delete Description", 1)
        cursor.execute(query, val)
        db_connection.commit()
        return super().setUp()
    
    def tearDown(self):
        query = 'DELETE FROM Skill WHERE skill_id=999999' 
        cursor.execute(query)
        db_connection.commit()

        query = 'DELETE FROM Skill WHERE skill_name="Edited Skill Name"' 
        cursor.execute(query)
        db_connection.commit()

        query = 'DELETE FROM Skill WHERE skill_name="skill"'
        cursor.execute(query)
        db_connection.commit()

        return super().tearDown()

    def test_view_skills(self):
        r = requests.get('http://localhost:5000/view_Skills')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.encoding, 'utf-8')
        self.assertEqual(type(r.json()['data']), list)
        self.assertEqual(type(r.json()['data'][0]), list)

    def test_get_CourseSkill(self):
        r = requests.get('http://localhost:5000/get_CourseSkill')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.encoding, 'utf-8')
        self.assertEqual(type(r.json()['data']), list)
        self.assertEqual(type(r.json()['data'][0]), list)


    def test_get_RoleSkill(self):
        r = requests.get('http://localhost:5000/get_RoleSkill')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.encoding, 'utf-8')
        self.assertEqual(type(r.json()['data']), list)

    def test_createSkill(self):
        r = requests.post('http://localhost:5000/create_Skill', json={"data":["skill", "this is the skill description"]})
        self.assertEqual(r.text, 'skill saved')
        self.assertEqual(r.status_code, 200)

    def test_deleteSkill(self):
        r = requests.delete('http://localhost:5000/delete_Skill/999999')
        self.assertEqual(r.text, 'skill 999999 deleted')
        self.assertEqual(r.status_code, 200)

    def test_switchStatus(self):
        data = {"data":[0]}
        r = requests.post('http://localhost:5000/switchStatus/999999', json = data)
        self.assertEqual(r.text, 'skill 999999 switched to 0')
        self.assertEqual(r.status_code, 200)

    def test_editSkill(self):
        data = {"data":[999999, "Edited Skill Name", "Edited Skill Description"]}
        r = requests.post('http://localhost:5000/edit_Skill', json=data)
        self.assertEqual(r.text, 'skill 999999 edited')
        self.assertEqual(r.status_code, 200)