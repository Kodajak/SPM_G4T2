==================
INSTALLATION GUIDE
==================

(1) set up and run a WAMP or MAMP server

(2) execute the contents of 'is212_example.sql' in phpMyAdmin, i.e. at:

       http://localhost/phpmyadmin  OR
	   http://localhost/phpMyAdmin

(3) find your web server's root directory (e.g. C:\wamp\www) and create a
    folder called 'is212'. Copy the contents of 'htdocs' into 'is212'.

(4) if you don't already have Flask installed, do:

	   python -m pip install flask
	   python -m pip install flask_cors
	   python -m pip install Flask-SQLAlchemy
	   python -m pip install mysql-connector-python

(5) in the 'flask' directory, run "python app.py" in a terminal.

(6) go to http://localhost/is212 where the application should be working!


===============
TROUBLESHOOTING
===============

If running the Flask application gives you an error message along the lines
of "ProgrammingError: (mysql.connector.errors.ProgrammingError) Character set
'255' unsupported", then the following temporary 'fix' will resolve it:

	   python -m pip install mysql-connector-python==0.29

