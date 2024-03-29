import sqlite3

try:
    db_connection = sqlite3.connect("src/db/users.db")
    db_create_table_query = """CREATE TABLE users (
        id TEXT PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        token TEXT NOT NULL,
        last_use_date TEXT NOT NULL);"""

    cursor = db_connection.cursor()
    cursor.execute(db_create_table_query)
    db_connection.commit()
    print("Table created")
    cursor.close()

except sqlite3.Error as error:
    print("Error while creating the db", error)

finally:
    if db_connection:
        db_connection.close()
