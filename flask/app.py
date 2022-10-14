from sqlite3 import Cursor
from urllib import response
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import mysql.connector as mysql



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

@app.route("/view_Skills")
def view_allSkills ():
    query = "SELECT * FROM Skill"
    cursor.execute(query)
    allSkills = cursor.fetchall()
    return jsonify(
        {
            "data": allSkills
        }
    ), 200

@app.route("/get_CourseSkill")
def get_CourseSkill ():
    query = "SELECT * FROM Course_Skill"
    cursor.execute(query)
    courseSkill = cursor.fetchall()
    return jsonify(
        {
            "data": courseSkill
        }
    ), 200

@app.route("/create_Skill", methods=['POST'])
def create_Skills():
    response_object = {'status': 'success'}
    data = {}
    if (request.method=='POST'):
        data = request.get_json()
        skill = data['data'][0]

        query2 = "INSERT INTO Skill (skill_desc, active) VALUES (%s, %s)"
        val = (skill, 1)
        cursor.execute(query2, val)
        db_connection.commit()
    else:
        response_object['msg']="error"
    return skill + ' saved'

@app.route("/delete_Skill/<int:id>", methods=['DELETE'])
def delete_Skill(id):
    response_object = {'status': 'success'}
    id = str(id)
    if (request.method=='DELETE'):
        query = "DELETE FROM Skill WHERE skill_id =" + id 
        cursor.execute(query)
        db_connection.commit()
    else:
        response_object['msg']="error"
    return 'skill' + id + ' deleted'

@app.route("/softDelete_Skill/<int:id>", methods=['POST'])
def softDelete_Skill(id):
    response_object = {'status': 'success'}
    id = str(id)
    if (request.method=='POST'):
        query = "UPDATE Skill SET active=0 WHERE skill_id=" + id
        cursor.execute(query)
        db_connection.commit()
    else:
        response_object['msg']="error"
    return 'skill' + id + ' deleted'

@app.route("/edit_Skill", methods=['GET', 'POST'])
def edit_Skill():
    response_object = {'status': 'success'}
    data = {}
    if (request.method=='POST'):
        data = request.get_json()
        skill_desc = data['data'][0][1]
        skill_id = str(data['data'][0][0])

        query = "UPDATE Skill SET skill_desc=%s WHERE skill_id=%s"
        val = (skill_desc, skill_id)
        cursor.execute(query, val)
        db_connection.commit()
    else:
        response_object['msg']="error"
    return 'skill ' + str(skill_id) + ' edited'

@app.route("/create_ljRoles", methods=['POST'])
def create_LJRole():
    response_object = {'status': 'success'}
    data = {}
    if (request.method=='POST'):
        data = request.get_json()
        role = data['data'][0]
        desc = data['data'][1]

        query2 = "INSERT INTO LJRole (ljrole_name, ljrole_desc) VALUES (%s, %s)"
        val = (role,desc)
        cursor.execute(query2, val)
        db_connection.commit()
    else:
        response_object['msg']="error"
    return role

# to pull out the course id that is under skills
def getCourse(course_id):
    query = "SELECT DISTINCT * FROM Course WHERE course_status='Active'" + "AND course_id ='" + str(course_id)+"'"
    cursor.execute(query)
    return cursor.fetchall()
# display it on html
@app.route("/view-course-skills/<int:skillID>")
def skill_by_course(skillID):

    query = "SELECT course_id FROM Course_Skill WHERE skill_id =" + str(skillID)
    cursor.execute(query)
    courseUnderSkill = cursor.fetchall()

    query = "SELECT skill_desc FROM Skill WHERE skill_id =" + str(skillID)
    cursor.execute(query)
    skill = cursor.fetchall()
    print(skill)
    courses = []
    for id in courseUnderSkill:
        courses.append(getCourse(id[0]))
    print(courses)
    
    return jsonify(
        {
            
            "data": courses,
            "skill":skill
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

        lj_data = (selectedRole[0], 'Incomplete')
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
        for course in selectedCourses:
            print(course[0])
            query2 = "INSERT INTO LJourney_Course VALUES (" + str(newLjId) + ","+ str(course[0]) + ")"
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
