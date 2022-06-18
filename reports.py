import database_functions
import mysql.connector
from tabulate import tabulate

class NevalidanUnos(Exception):
    def __init__(self, message=None):
        self.message = message
        
    def __str__(self):
        if self.message is None:
            return "Nevalidan unos."
        return self.message

def izvestaj_ulica(ulica, baza):
    baza = database_functions.konekcija()
    lista = list()
    lista.append(ulica)
    my_cursor = baza.cursor() 

    try:
        my_cursor.execute("SELECT brojilo.ulica, sum(potrosnja_brojila.potrosnja), potrosnja_brojila.mesec FROM baza_podataka.potrosnja_brojila JOIN baza_podataka.brojilo WHERE brojilo.id = potrosnja_brojila.id AND brojilo.ulica = %s GROUP BY potrosnja_brojila.mesec", lista)
        rezultat = my_cursor.fetchall()
    except mysql.connector.Error:
        print("Greska prilikom izvrsavanja upita u bazi.")
        return None

    return rezultat

def izvestaj_brojilo(brojilo, baza):
    lista = list()
    lista.append(brojilo)
    my_cursor = baza.cursor()
    try:
        my_cursor.execute("SELECT brojilo.id, potrosnja_brojila.potrosnja, potrosnja_brojila.mesec FROM baza_podataka.potrosnja_brojila JOIN baza_podataka.brojilo WHERE brojilo.id = potrosnja_brojila.id AND brojilo.id = %s GROUP BY potrosnja_brojila.mesec;", lista)
        rezultat = my_cursor.fetchall()
    except mysql.connector.Error:
        print("Greska prilikom izvrsavanja upita u bazi.")
        return None
    
    return rezultat

def izvestaj_ispis(rezultat):
    redovi = list()
    
    if rezultat == None:
        print("Ne postoji trazeni izvestaj.")
    else:
        head = ["Mesec", "Potrosnja"]
        for red in rezultat:
            redovi.append([red[2], red[1]])
                
        print(tabulate(redovi, headers=head, tablefmt="grid"))
        
def meni(odgovor):
    
    try:
        odgovor = int(odgovor)
        if odgovor <= 0 or odgovor > 3:
            raise NevalidanUnos("Unesite 1, 2 ili 3.")
        
        return odgovor
    except NevalidanUnos as e:
        print(e)
        return None
    except Exception:
        print("Unesite broj.")
        return None
    
def izvestaj(odgovor, baza):
    
    try:
        if odgovor == 1:
        
            ulica = input("Unesite ulicu: ")
            
            if ulica.isdigit():
                raise NevalidanUnos("Ulica mora biti string.")
            if type(ulica) != str:
                raise NevalidanUnos("Ulica mora biti string.")
            
            rezultat = izvestaj_ulica(ulica, baza)
            if len(rezultat) == 0:
                raise NevalidanUnos("Ulica ne postoji.")
            izvestaj_ispis(rezultat)
            rezultat.clear()
            return
        elif odgovor == 2:
            brojilo = int(input("Unesite brojilo: "))
            rezultat = izvestaj_brojilo(brojilo, baza)
            if len(rezultat) == 0:
                raise NevalidanUnos("Brojilo ne postoji.")
            izvestaj_ispis(rezultat)
            rezultat.clear()
            return
    except NevalidanUnos as poruka:
        print(poruka)
        return None
    except Exception:
        print("ID brojila mora biti broj.")
        return None
        
        
def main():
    baza = database_functions.konekcija()
    
    while True:
        print("Meni\n1 - Izvestaj mesecne postrosnje za ulicu\n2 - Izvestaj mesecne potrosnje za brojilo\n3 - Izlaz")
        rezultat = list()
        
        odgovor = meni(input())
        
        if odgovor == None:
            continue
        elif odgovor == 3:
            break

        odgovor_izvestaja = izvestaj(odgovor, baza)
        
        if odgovor_izvestaja == None:
            continue
        
if __name__ == "__main__":
    main()
