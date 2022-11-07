from flask import Flask, request, jsonify, request, Blueprint
from flask_cors import CORS
import mysql.connector as mysql

skillManagementFunctions = Blueprint('skillManagementFunctions', __name__)

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

CORS(skillManagementFunctions)


# --------- Skills Management Functions ---------
# -------------------- Start --------------------

# [START] Function to GET ALL skills
@skillManagementFunctions.route("/view_Skills")
def view_allSkills ():
    query = "SELECT * FROM Skill"
    cursor.execute(query)
    allSkills = cursor.fetchall()
    return jsonify(
        {
            "data": allSkills
        }
    ), 200
# [START] Function to GET ALL skills details

# [START] Function to GET ALL Course ID linked to Skill ID
@skillManagementFunctions.route("/get_CourseSkill")
def get_CourseSkill():
    query = "SELECT * FROM Course_Skill"
    cursor.execute(query)
    courseSkill = cursor.fetchall()
    return jsonify(
        {
            "data": courseSkill
        }
    ), 200
# [END] Function to GET ALL Course ID linked to Skill ID

# [START] Function to GET ALL learning journey role ID linked to Skill ID
@skillManagementFunctions.route("/get_RoleSkill")
def get_RoleSkill():
    query = "SELECT * FROM LJRole_Skill"
    cursor.execute(query)
    roleSkill = cursor.fetchall()
    return jsonify(
        {
            "data": roleSkill
        }
    ), 200
# [END] Function to GET ALL learning journey role ID linked to Skill ID

# [START] Function to CREATE a skill
@skillManagementFunctions.route("/create_Skill", methods=['POST'])
def create_Skills():
    response_object = {'status': 'success'}
    data = {}
    if (request.method=='POST'):
        data = request.get_json()
        skillName = data['data'][0]
        skillDesc = data['data'][1]

        query2 = "INSERT INTO Skill (skill_name, skill_desc, status) VALUES (%s, %s, %s)"
        val = (skillName, skillDesc, 1)
        cursor.execute(query2, val)
        db_connection.commit()
    else:
        response_object['msg']="error"
    return skillName + ' saved'
# [END] Function to CREATE a skill

# [START] Function to DELETE a skill based on sepcified skill ID
@skillManagementFunctions.route("/delete_Skill/<int:id>", methods=['DELETE'])
def delete_Skill(id):
    response_object = {'status': 'success'}
    id = str(id)
    if (request.method=='DELETE'):
        query = "DELETE FROM Skill WHERE skill_id =" + id 
        cursor.execute(query)
        db_connection.commit()
    else:
        response_object['msg']="error"
    return 'skill ' + id + ' deleted'
# [END] Function to DELETE a skill based on sepcified skill ID

# [START] Function to SOFT DELETE a skill based on sepcified skill ID
@skillManagementFunctions.route("/switchStatus/<int:id>", methods=['POST'])
def switchStatus(id):
    response_object = {'status': 'success'}
    id = str(id)
    data = {}
    if (request.method=='POST'):
        data = request.get_json()
        if (data['data'][0] == 0):
            query = "UPDATE Skill SET status=0 WHERE skill_id=" + id
        else:
            query = "UPDATE Skill SET status=1 WHERE skill_id=" + id

        cursor.execute(query)
        db_connection.commit()
    else:
        response_object['msg']="error"
    return 'skill ' + id + ' switched to ' + str(data['data'][0])
# [END] Function to SOFT DELETE a skill based on sepcified skill ID

# [START] Function to EDIT a skill based on sepcified skill ID
@skillManagementFunctions.route("/edit_Skill", methods=['GET', 'POST'])
def edit_Skill():
    response_object = {'status': 'success'}
    data = {}
    if (request.method=='POST'):
        data = request.get_json()
        skill_name = data['data'][1]
        skill_desc = data['data'][2]
        skill_id = str(data['data'][0])

        query = "UPDATE Skill SET skill_name=%s, skill_desc=%s WHERE skill_id=%s"
        val = (skill_name, skill_desc, skill_id)
        cursor.execute(query, val)
        db_connection.commit()
    else:
        response_object['msg']="error"
    return 'skill ' + str(skill_id) + ' edited'
# [END] Function to EDIT a skill based on sepcified skill ID

# -------- Skills Management Functions --------
# -------------------- End --------------------
