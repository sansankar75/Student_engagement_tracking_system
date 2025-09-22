import mysql.connector

# Establish connection
mydb = mysql.connector.connect(
    host="127.0.0.1",     # or your MySQL server IP
    user="san",          # your MySQL username
    password="",  # your MySQL password
    database="arun"     # optional: database name
)

# Create a cursor
cursor = mydb.cursor()

# Example: create a table
cursor.execute("CREATE TABLE IF NOT EXISTS students (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), age INT)")

# Example: insert data
sql = "INSERT INTO students (name, age) VALUES (%s, %s)"
val = ("John", 21)
cursor.execute(sql, val)
mydb.commit()

print(cursor.rowcount, "record inserted.")

# Example: fetch data
cursor.execute("SELECT * FROM students")
result = cursor.fetchall()
for row in result:
    print(row)

# Close connection
mydb.close()
