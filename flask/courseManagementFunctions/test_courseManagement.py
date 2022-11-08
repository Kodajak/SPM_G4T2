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

class TestCourseManagement(unittest.TestCase):

    def setUp(self):

        return super().setUp()
    
    def tearDown(self):

        return super().tearDown()

    def test_statusOfImportUnCom(self):
        r = requests.get('http://localhost:5000/statusOfImportUnCom')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['msg'], 'Unable to commit to database !')

    def test_statusOfImportDup(self):
        r = requests.get('http://localhost:5000/statusOfImportDup')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['msg'], 'Duplicated courses found ! Import Fail !')

    def test_statusOfImportSuc(self):
        r = requests.get('http://localhost:5000/statusOfImportSuc')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['msg'], 'Successfully imported courses !')

    def test_statusOfImportOnl(self):
        r = requests.get('http://localhost:5000/statusOfImportOnl')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['msg'], 'Import only course.csv !')
