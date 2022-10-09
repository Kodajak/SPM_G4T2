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

# get skills based on selected ljRole id
@app.route("/view_skills/<int:ljRole_Id>")
def view_skills(ljRole_Id):
    query = "SELECT LJR.ljrole_id, LJR.ljrole_name, LJR.ljrole_desc, All_skills.skill_id, All_skills.skill_desc, All_skills.Active FROM ((spmDB.LJRole LJR INNER JOIN spmDB.LJRole_Skill LJR_Skill ON LJR.ljrole_id = LJR_Skill.ljrole_id) INNER JOIN spmDB.Skill All_skills ON LJR_Skill.skill_id = All_skills.skill_id)"
    cursor.execute(query)
    skills = cursor.fetchall()
    filteredSkills = []
    for skill in skills:
        if skill[0] == ljRole_Id:
            filteredSkills.append([skill[3],skill[4], skill[5]])
    return jsonify(
        {
            "data": filteredSkills
        }
    ), 200

# get new learning journey ID
def getLjId():
    query = "SELECT MAX(ljourney_id) FROM LearningJourney"
    cursor.execute(query)
    data = cursor.fetchall()
    id = data[0][0]
    return id

@app.route("/create_lj", methods=["POST"])
def create_lj():
    # check for missing inputs
    data = request.get_json()
    print(data)
    if not all(key in data.keys() for
               key in ('selectedRole', 'selectedCourses')):
        return jsonify({
            "message": "Incorrect JSON object provided."
        }), 500
  
    # if form validation succesful
    try:
    # sample_query = "SELECT ljrole_id FROM LearningJourney"
    # cursor.execute(sample_query)
    # id = cursor.fetchall()
    # print(id)
    # count = len(id) + 1
    # print(count)
    # sampleRoleId = 22
    # completionStatus = 'Incomplete'

        selectedRole = data['selectedRole']
        print(selectedRole)
        print(type(selectedRole))
        query = "INSERT INTO LearningJourney (ljrole_id, completion_status) VALUES (%s, %s);"

        lj_data = (selectedRole, 'Incomplete')
        cursor.execute(query, lj_data)
        db_connection.commit()
        print("pass 1")

        sample_query = "SELECT * FROM LearningJourney"
        cursor.execute(sample_query)
        print(cursor.fetchall())

        # get new learning journey Id
        newLjId = getLjId()

        print(newLjId)
        selectedCourses = data['selectedCourses']   
        for courseId in selectedCourses:
            print(courseId)
            query2 = "INSERT INTO LJourney_Course VALUES (" + str(newLjId) + ","+ str(courseId) + ")"
            cursor.execute(query2)
            db_connection.commit()
        print("completed")

        sample_query2 = "SELECT * FROM LJourney_Course"
        cursor.execute(sample_query2)
        print(cursor.fetchall())
        return jsonify("success"), 201

    except Exception:
        return jsonify({
            "message": "Unable to commit to database."
        }), 500

# sample
# @app.route("/consultations", methods=['POST'])
# def create_consultation():
#     data = request.get_json()
#     if not all(key in data.keys() for
#                key in ('doctor_id', 'patient_id',
#                        'diagnosis', 'prescription', 'length')):
#         return jsonify({
#             "message": "Incorrect JSON object provided."
#         }), 500

#     # (1): Validate doctor
#     doctor = Doctor.query.filter_by(id=data['doctor_id']).first()
#     if not doctor:
#         return jsonify({
#             "message": "Doctor not valid."
#         }), 500

#     # (2): Compute charges
#     charge = doctor.calculate_charges(data['length'])

#     # (3): Validate patient
#     patient = Patient.query.filter_by(id=data['patient_id']).first()
#     if not patient:
#         return jsonify({
#             "message": "Patient not valid."
#         }), 500

#     # (4): Subtract charges from patient's e-wallet
#     try:
#         patient.ewallet_withdraw(charge)
#     except Exception:
#         return jsonify({
#             "message": "Patient does not have enough e-wallet funds."
#         }), 500

#     # (4): Create consultation record
#     consultation = Consultation(
#         diagnosis=data['diagnosis'], prescription=data['prescription'],
#         doctor_id=data['doctor_id'], patient_id=data['patient_id'],
#         charge=charge
#     )

#     # (5): Commit to DB
#     try:
#         db.session.add(consultation)
#         db.session.commit()
#         return jsonify(consultation.to_dict()), 201
#     except Exception:
#         return jsonify({
#             "message": "Unable to commit to database."
#         }), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
