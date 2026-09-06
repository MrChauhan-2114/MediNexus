import mysql.connector


def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Chauhan@211420",
        database="healthcare_db"
    )

    return connection

