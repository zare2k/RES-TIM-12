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
        
def dodaj_element(id_brojila, potrosnja_vode, mesec, baza):
    my_cursor = baza.cursor()
    my_cursor.execute("INSERT INTO potrosnja_brojila (id, potrosnja, mesec) VALUES (%s, %s, %s)", (id_brojila, potrosnja_vode, mesec))
    baza.commit()

def provera_id(id_brojila, baza):
    my_cursor = baza.cursor()
    lista = list()
    lista.append(id_brojila)
    my_cursor.execute("SELECT * FROM baza_podataka.brojilo WHERE brojilo.id = %s", id_brojila)
    rezultat = my_cursor.fetchall()
    return rezultat

def provera_mesec(id_brojila, mesec, baza):
    my_cursor = baza.cursor()
    my_cursor.execute("SELECT * FROM baza_podataka.potrosnja_brojila WHERE potrosnja_brojila.id = %s and potrosnja_brojila.mesec = %s", (id_brojila, mesec))
    rezultat = my_cursor.fetchall()
    return rezultat
