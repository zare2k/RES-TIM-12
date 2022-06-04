import mysql.connector

def konekcija():
    baza = mysql.connector.connect(
        host = "localhost",
        database = "baza_podataka",
        user = "root",
        password = "student")
    
    if baza.is_connected():
        print('Uspesna konekcija na bazu podataka!')
        
    return baza
        
def dodaj_element(id_brojila, potrosnja_vode, baza):
    myCursor = baza.cursor()
    myCursor.execute("INSERT INTO baza_podataka (id, potrosnja) VALUES (%s, %s)", (id_brojila, potrosnja_vode))
    baza.commit()