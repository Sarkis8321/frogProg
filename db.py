import sqlite3

conn = sqlite3.connect("data-test.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE abitur (surname text, name text, patr text, birth text)""")
