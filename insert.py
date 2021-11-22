import sqlite3

conn = sqlite3.connect("data-test.db")
cursor = conn.cursor()

cursor.execute("""
    INSERT INTO abitur(surname, name, patr, birth)
    VALUES("Коваленко", "Сергей","Александрович","22.10.2000")
""")
conn.commit()