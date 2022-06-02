import  mysql.connector

baza = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password="student"
)

myCursor=baza.cursor()
def napravi_bazu():
  myCursor.execute("CREATE DATABASE baza_podataka")
  
  
napravi_bazu()