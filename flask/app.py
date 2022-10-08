from sqlite3 import Cursor
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import mysql.connector as mysql
import requests
import json


app = Flask(__name__)
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

CORS(app)

@app.route('/')
def home():
    return "Hello"

@app.route("/view_roles")
def view_Role():
    query = "SELECT * FROM Role"
    cursor.execute(query)
    roles = cursor.fetchall()
    return jsonify(
        {
            "data": dict(role for role in roles)
        }
    ), 200

@app.route("/view_ljRoles")
def view_LJRole ():
    query = "SELECT * FROM LJRole"
    cursor.execute(query)
    ljRoles = cursor.fetchall()
    return jsonify(
        {
            "data": ljRoles
        }
    ), 200

# to pull out the course id that is under skills
def getCourse(course_id):
    query = "SELECT * FROM Course where course_id =" + str(course_id)
    cursor.execute(query)
    return cursor.fetchall()
# display it on html
@app.route("/view-course-skills/<int:skillID>")
def skill_by_course(skillID):

    query = "SELECT course_id FROM Course_Skill where skill_id =" + str(skillID)
    cursor.execute(query)
    courseUnderSkill = cursor.fetchall()
    courses = []
    for id in courseUnderSkill:
        courses.append(getCourse(id[0]))
    print(courses)
    
    return jsonify(
        {
            
            "data": courses
            # "data": {
            #     "courses": [course.json() for course in course_skills]
            # }
        }
    )
@app.route("/create_lj", methods=["POST"])
def create_lj():
    # check for missing inputs
    data = request.get_json()
    if not all(key in data.keys() for
               key in ('selectedRole', 'selectedCourses')):
        return jsonify({
            "message": "Incorrect JSON object provided."
        }), 500
  
    # if form validation succesful
    try:
        selectedRole = data['selectedRole']
        query = "INSERT INTO LearningJourney (ljrole_id, completion_status) VALUES (" + selectedRole + ", 'Incomplete')"
        cursor.execute(query)

    except Exception:
        return jsonify({
            "message": "Unable to commit to database."
        }), 500

def create_lj():
    # check for missing inputs
    data = request.get_json()
    if not all(key in data.keys() for
               key in ('selectedRole', 'selectedCourses')):
        return jsonify({
            "message": "Incorrect JSON object provided."
        }), 500
  
    # if form validation succesful, create a table for each course
    try:
        # get new learning journey id
        query = "SELECT ljourney_id FROM LearningJourney \
                WHERE ljourney_id = ( \
                    SELECT IDENT_CURRENT('LearningJourney'))"
        cursor.execute(query)
        ljourney_Id = cursor.fetchall()

        # get selected courses
        selectedCourses = data['selectedCourses']

        # populate new row for each course selected
        for courseId in selectedCourses:
            query = "INSERT INTO courseId VALUES (" + ljourney_Id + "," + courseId + ")"
            cursor.execute(query)
        
    except Exception:
        return jsonify({
            "message": "Unable to commit to database."
        }), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
