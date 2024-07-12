import mysql.connector

from utils import upload_file_to_s3
from datetime import datetime


# Function to connect to MySQL database
def connect_to_mysql():
    return mysql.connector.connect(
        host="101.42.92.57",
        user="root",
        password="ZRSz2580",
        database="old"
    )


# Event model class
class Event:
    def __init__(self, type, time, location, image=None):
        self.type = type
        self.time = time
        self.location = location
        self.image = image

    def __repr__(self):
        return f'<Event {self.id}: {self.type}>'

    @classmethod
    def create(cls, type, location, image):
        upload_file_to_s3(image)
        # Connect to MySQL database
        conn = connect_to_mysql()
        cursor = conn.cursor()
        current_time = datetime.now()
        # Format current_time as a string in MySQL datetime format
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        # SQL query to insert event
        insert_query = """INSERT INTO event (type, time, location, image) 
                          VALUES (%s, %s, %s, %s)"""
        event_data = (type, formatted_time, location, image)
        try:
            # Execute the query
            cursor.execute(insert_query, event_data)
            conn.commit()
            print("Event successfully created")
            # Return the created Event instance (not used in this example)
            new_event = cls(type, formatted_time, location, image)
            return new_event

        except mysql.connector.Error as error:
            print(f"Failed to insert event: {error}")

        finally:
            # Close cursor and connection
            cursor.close()
            conn.close()

    @classmethod
    def list_all(cls):
        # Connect to MySQL database
        conn = connect_to_mysql()
        cursor = conn.cursor()
        # SQL query to select all events
        select_query = "SELECT * FROM event"

        try:
            # Execute the query
            cursor.execute(select_query)
            # Fetch all rows from the last executed statement
            events = cursor.fetchall()
            # Convert tuple list to dict list
            events = [dict(zip(cursor.column_names, event)) for event in events]
            # Format time for each event
            for event in events:
                # Format datetime object to string in the format you want
                event['time'] = event['time'].strftime('%Y/%m/%d %H:%M:%S')
            return events

        except mysql.connector.Error as error:
            print(f"Failed to select events: {error}")

        finally:
            # Close cursor and connection
            cursor.close()
            conn.close()


class Oldman:
    def __init__(self, id, room, name, age, gender, image, phone, type):
        self.id = id
        self.room = room
        self.name = name
        self.age = age
        self.gender = gender
        self.image = image
        self.phone = phone
        self.type = type

    def __repr__(self):
        return f'<Oldman {self.id}: {self.name}>'

    @classmethod
    def create(cls, name, room, age, gender, image, phone, type):
        upload_file_to_s3(image)
        # Connect to MySQL database
        conn = connect_to_mysql()
        cursor = conn.cursor()
        # SQL query to insert oldman
        insert_query = """INSERT INTO oldman ( name,room, age, gender, image, phone,type) 
                          VALUES (%s, %s, %s, %s, %s, %s,%s)"""
        oldman_data = (name, room, age, gender, image, phone, type)
        try:
            # Execute the query
            cursor.execute(insert_query, oldman_data)
            conn.commit()
            print("Oldman successfully created")
            # Return the created Oldman instance (not used in this example)
            new_oldman = cls(None, room, name, age, gender, image, phone, type)
            return new_oldman
        except mysql.connector.Error as error:
            print(f"Failed to insert oldman: {error}")
        finally:
            # Close cursor and connection
            cursor.close()
            conn.close()

    @classmethod
    def list_all(cls):
        # Connect to MySQL database
        conn = connect_to_mysql()
        cursor = conn.cursor()
        # SQL query to select all oldman
        select_query = "SELECT * FROM oldman"

        try:
            # Execute the query
            cursor.execute(select_query)
            # Fetch all rows from the last executed statement
            oldmen = cursor.fetchall()
            # Convert tuple list to dict list
            oldmen = [dict(zip(cursor.column_names, oldman)) for oldman in oldmen]
            return oldmen
        except mysql.connector.Error as error:
            print(f"Failed to select oldman: {error}")
        finally:
            # Close cursor and connection
            cursor.close()
            conn.close()
