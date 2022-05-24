import sqlite3

# Source: https://www.javatpoint.com/python-sqlite
connection = sqlite3.connect('detections.db')

def create_tables():
    connection.execute('''CREATE TABLE IF NOT EXISTS DETECTIONS (ID INTEGER PRIMARY KEY AUTOINCREMENT, 
    TIMESTAMP TEXT NOT NULL, ROOM_NR TEXT NOT NULL, VIDEO_FILE_NAME TEXT NOT NULL);''')
    connection.commit()

def add_detection(timestamp, room_nr, video_file_name):
    connection.execute('''INSERT INTO DETECTIONS (TIMESTAMP, ROOM_NR, VIDEO_FILE_NAME) \
    VALUES ("'''+str(timestamp)+'''","'''+str(room_nr)+'''","'''+str(video_file_name)+'''");''')
    connection.commit()

def get_detections():
    results = connection.execute('''SELECT * FROM DETECTIONS''').fetchall()
    list_string = ""
    for result in results:
        list_string = list_string + str(result) + "\n"
    return list_string

def close_connection():
    connection.close()

create_tables()