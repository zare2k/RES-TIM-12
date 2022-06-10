import mysql.connector

def konekcija():
    baza = mysql.connector.connect(
        host = "localhost",
        database = "baza_podataka",
        user = "root",
        password = "student")
        
    return baza
        
def dodaj_element(id_brojila, potrosnja_vode, mesec, baza): 
    myCursor = baza.cursor()
    myCursor.execute("INSERT INTO potrosnja_brojila (id, potrosnja, mesec) VALUES (%s, %s, %s)", (id_brojila, potrosnja_vode, mesec))
    baza.commit()
