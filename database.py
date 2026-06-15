import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root28",
    database="bus_booking_bd"
)
cursor = mydb.cursor(buffered=True)

print("Database connected successfully")