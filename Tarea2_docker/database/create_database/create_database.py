import mysql.connector
import os, time

def create_database(db_connection,db_name,cursor):
	cursor.execute(f"CREATE DATABASE {db_name};")
	cursor.execute(f"COMMIT;")
	cursor.execute(f"USE {db_name};")

	cursor.execute("SET GLOBAL time_zone = 'UTC';")
	cursor.execute("SET SESSION time_zone = 'UTC';")

	cursor.execute("COMMIT;") 

#######################
DATABASE = "tutorial_2"

DATABASE_IP = str(os.environ['DATABASE_IP'])

DATABASE_USER = "root"
DATABASE_USER_PASSWORD = "root"

not_connected = True

while(not_connected):
	try:
		print(DATABASE_IP,"IP")
		db_connection = mysql.connector.connect(user=DATABASE_USER,host=DATABASE_IP,password=DATABASE_USER_PASSWORD)
		not_connected = False

	except Exception as e:
		time.sleep(3)
		print(e, "error!!!")
		print("can't connect to mysql server, might be intializing")
		
cursor = db_connection.cursor()

try:
	cursor.execute(f"USE {DATABASE}")
	print(f"Database: {DATABASE} already exists")
except Exception as e:
    create_database(db_connection,DATABASE,cursor)
    print(f"Succesfully created: {DATABASE}")
