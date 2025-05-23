import sqlite3
conn = sqlite3.connect("iris.db")
print("opened database successfully")

conn.execute("CREATE TABLE diginadmin (amail varchar,apassword varchar)")
conn.execute("CREATE TABLE addfaq (question varchar,answer varchar)")

conn.execute("CREATE TABLE signup (uname varchar,uphone varchar,username varchar,upassword varchar)")
conn.execute("CREATE TABLE predict (petallength Number,petalwidth Number,sepallength Number, sepalwidth Number,result varchar)")

print("table created successfully")
conn.close()
    