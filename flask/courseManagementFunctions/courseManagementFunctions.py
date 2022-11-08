from flask import Flask, request, jsonify, request, Blueprint
from flask_cors import CORS
import mysql.connector as mysql

courseManagementFunctions = Blueprint('courseManagementFunctions', __name__)

# enter your server IP address/domain name
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
# enter your code here!

cursor = db_connection.cursor()

CORS(courseManagementFunctions)

# --------- Course Management Functions ---------
# -------------------- Start --------------------

# [START] Function to Redirect and show CSV Import Status on HTML
@courseManagementFunctions.route("/statusOfImportUnCom")
def statusOfImportUnCom():
    return jsonify(
        {
            "msg": "Unable to commit to database !"
        }
    )
@courseManagementFunctions.route("/statusOfImportDup")
def statusOfImportDup():
    return jsonify(
        {
            "msg": "Duplicated courses found ! Import Fail !"
        }
    )
@courseManagementFunctions.route("/statusOfImportSuc")
def statusOfImportSuc():
    return jsonify(
        {
            "msg": "Successfully imported courses !"
        }
    )
@courseManagementFunctions.route("/statusOfImportOnl")
def statusOfImportOnl():
    return jsonify(
        {
            "msg": "Import only course.csv !"
        }
    )
# [START] Function to Redirect and show CSV Import Status on HTML

# [START] Function to GET all courses
@courseManagementFunctions.route("/view-course-list")
def courses():
    query = "SELECT * FROM Course"
    cursor.execute(query)
    courseUnderSkill = cursor.fetchall()

    return jsonify(
        {
            "courses": courseUnderSkill
        }
    )
# [END] Function to GET all courses

# --------- Course Management Functions ---------
# -------------------- END --------------------