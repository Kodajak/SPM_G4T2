from flask import Flask, request, jsonify, request, Blueprint, redirect
from flask_cors import CORS
import mysql.connector as mysql
import pandas as pd
import os


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

# [START] Function to convert CSV file to insert data into Database
def parseCSV(filePath):
   # CVS Column Names
    col_names = ['Course_ID', 'Course_Name', 'Course_Desc', 'Course_Status', 'Course_Type', 'Course_Category']
    # Use Pandas to parse the CSV file
    csvData = pd.read_csv(filePath, names = col_names, header = None, encoding= 'unicode_escape', skiprows=1)
    # Loop through the Rows

    for i, row in csvData.iterrows():
        sql = "INSERT INTO Course_Test (Course_ID, Course_Name, Course_Desc, Course_Status, Course_Type, Course_Category) VALUES (%s, %s, %s, %s, %s, %s)"
        value = (row['Course_ID'], row['Course_Name'], row['Course_Desc'], row['Course_Status'], row['Course_Type'], row['Course_Category'])
        cursor.execute(sql, value)
        db_connection.commit()
        print(value)
# [END] Function to convert CSV file to insert data into Database

# [START] Function to IMPORT all courses from CSV file
@courseManagementFunctions.route("/import_csv", methods=['POST'])
def uploadFiles():
   # get the uploaded file
    if('file' in request.files):
        uploaded_file = request.files['file']
        if uploaded_file.filename == 'courses.csv':
            # set the file path
            file_path = os.path.join(courseManagementFunctions.config['UPLOAD_FOLDER'], uploaded_file.filename)
            # save the file
            uploaded_file.save(file_path)
            try:
                parseCSV(file_path)
                return redirect("http://localhost:8888/SPMProject/SPM%2520Project/htdocs/statusOfImportSuc.html")
            except mysql.errors.IntegrityError:
                return redirect("http://localhost:8888/SPMProject/SPM%2520Project/htdocs/statusOfImportDup.html")
            except Exception:
                return redirect("http://localhost:8888/SPMProject/SPM%2520Project/htdocs/statusOfImportUnCom.html")
        else:
                return redirect("http://localhost:8888/SPMProject/SPM%2520Project/htdocs/statusOfImportOnl.html")
    else:
        return redirect("http://localhost:8888/SPMProject/SPM%2520Project/htdocs/coursesManagement.html")

# [END] Function to IMPORT all courses from CSV file

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