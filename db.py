import sqlite3
def fetch():
    database_connection = sqlite3.connect("quizitDatabase.db")
    database_cursor = database_connection.cursor()
    data=database_cursor.execute("select * from register_admin;")
    database_connection.commit()
    database_connection.close()
    return data