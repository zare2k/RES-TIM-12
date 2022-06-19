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
        return "ERROR"
    else:
        head = ["Mesec", "Potrosnja"]
        for red in rezultat:
            redovi.append([red[2], red[1]])
                
        print(tabulate(redovi, headers=head, tablefmt="grid"))
        return "OK"
        
def meni():
    print("Meni\n1 - Izvestaj mesecne postrosnje za ulicu\n2 - Izvestaj mesecne potrosnje za brojilo\n3 - Izlaz")
    odgovor = input()
    
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
    
def unos_ulica():
    ulica = input("Unesite ulicu: ")
            
    try:
        if ulica.isdigit():
            raise NevalidanUnos("Ulica mora biti string.")
        
        return ulica
    except NevalidanUnos as e:
        print(e)

def unos_brojilo():
    
    try:
        brojilo = int(input("Unesite brojilo: "))
        if brojilo <= 0:
            raise NevalidanUnos
        
        return brojilo

    except NevalidanUnos as poruka:
        print(poruka)
        return None
    except Exception:
        print("ID brojila mora biti broj.")
        return None
    
def duzina_liste(rezultat):
    return len(rezultat)
    
def izvestaj(odgovor, baza):
    rezultat = list()

    try:
        if odgovor == 1:
                
            ulica = unos_ulica()
            if ulica == None:
                return None

            rezultat = izvestaj_ulica(ulica, baza)
            if duzina_liste(rezultat) == 0:
                raise NevalidanUnos("Ulica ne postoji.")
            izvestaj_ispis(rezultat)
            return "OK"
        
        elif odgovor == 2:
                    
            brojilo = unos_brojilo()
            if brojilo == None:
                return None
            
            rezultat = izvestaj_brojilo(brojilo, baza)
            if duzina_liste(rezultat) == 0:
                raise NevalidanUnos("Brojilo ne postoji.")
            izvestaj_ispis(rezultat)
            return "OK"

    except NevalidanUnos as e:
        print(e)
        
def main(baza, odgovor):
        
    if odgovor == None:
        return None
    elif odgovor == 3:
        return "EXIT"

    if izvestaj(odgovor, baza) == None:
        return None

if __name__ == "__main__":
    baza = database_functions.konekcija()
    
    while True:
        odgovor = meni()
        if main(baza, odgovor) == "EXIT":
            break
