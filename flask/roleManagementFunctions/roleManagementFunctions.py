from flask import Flask, request, jsonify, request, Blueprint
from flask_cors import CORS
import mysql.connector as mysql

roleManagementFunctions = Blueprint('roleManagementFunctions', __name__)

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

CORS(roleManagementFunctions)

# --------- Roles Management Functions ---------
# -------------------- Start --------------------

# [START] Function to GET ALL learning journey roles
@roleManagementFunctions.route("/view_ljRoles")
def view_LJRole ():
    query = "SELECT * FROM LJRole"
    cursor.execute(query)
    ljRoles = cursor.fetchall()
    return jsonify(
        {
            "data": ljRoles
        }
    ), 200
# [END] Function to GET ALL learning journey roles

# [START] Function to SOFT DELETE a learning journey role based on a specified learning journey role ID
@roleManagementFunctions.route("/softDelete_ljrole", methods=['POST'])
def softDelete_role():
    response_object = {'status': 'success'}
    if (request.method=='POST'):
        data = request.get_json()
        id = str(data['data'][0][0])
        stat = data['data'][0][3]
        if(stat==1):
            stat=0
        else:
            stat=1
        query = "UPDATE LJRole SET status="+str(stat)+" WHERE ljrole_id= " + id
        cursor.execute(query)
        db_connection.commit()
    else:
        response_object['msg']="error"
    return 'ljrole' + id + ' status changed'
# [END] Function to SOFT DELETE a learning journey role based on a specified learning journey role ID

# [START] Function to EDIT a learning journey role based on a specified learning journey role ID
@roleManagementFunctions.route("/edit_Role", methods=['GET', 'POST'])
def edit_Role():
    response_object = {'status': 'success'}
    data = {}
    if (request.method=='POST'):
        data = request.get_json()
        role_name = data['data'][0][1]
        role_desc = data['data'][0][2]
        role_id = str(data['data'][0][0])

        query = "UPDATE LJRole SET ljrole_name=%s, ljrole_desc=%s WHERE ljrole_id=%s"
        val = (role_name, role_desc, role_id)
        cursor.execute(query, val)
        db_connection.commit()
    else:
        response_object['msg']="error"
    return 'role ' + str(role_id) + ' edited'
# [END] Function to EDIT a learning journey role based on a specified learning journey role ID

# [START] Function to CREATE a learning journey role based on a specified learning journey role ID
@roleManagementFunctions.route("/create_ljRoles", methods=['POST'])
def create_LJRole():
    response_object = {'status': 'success'}
    data = {}
    if (request.method=='POST'):
        data = request.get_json()
        role = data['data'][0]
        desc = data['data'][1]

        query2 = "INSERT INTO LJRole (ljrole_name, ljrole_desc, status) VALUES (%s, %s,%s)"
        val = (role,desc,1)
        cursor.execute(query2, val)
        db_connection.commit()
    else:
        response_object['msg']="error"
    return role
# [END] Function to CREATE a learning journey role based on a specified learning journey role ID

# --------- Roles Management Functions ---------
# -------------------- End ---------------------
