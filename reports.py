import database_functions

def izvestaj_ulica(ulica):
    baza = database_functions.konekcija()
    lista = list()
    lista.append(ulica)
    myCursor = baza.cursor() 
    myCursor.execute("SELECT brojilo.ulica, sum(potrosnja_brojila.potrosnja), potrosnja_brojila.mesec FROM baza_podataka.potrosnja_brojila JOIN baza_podataka.brojilo WHERE brojilo.id = potrosnja_brojila.id AND brojilo.ulica = %s GROUP BY potrosnja_brojila.mesec", lista)
    rezultat = myCursor.fetchall()
    return rezultat

def izvestaj_brojilo(brojilo):
    baza = database_functions.konekcija()
    lista = list()
    lista.append(brojilo)
    myCursor = baza.cursor()
    myCursor.execute("SELECT brojilo.id, potrosnja_brojila.potrosnja, potrosnja_brojila.mesec FROM baza_podataka.potrosnja_brojila JOIN baza_podataka.brojilo WHERE brojilo.id = potrosnja_brojila.id AND brojilo.id = %s GROUP BY potrosnja_brojila.mesec;", lista)
    rezultat = myCursor.fetchall()
    return rezultat
