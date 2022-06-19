import socket
import podatak
import pickle

class NevalidanUnos(Exception):
    def __init__(self, message=None):
        self.message = message
        
    def __str__(self):
        if self.message is None:
            return "Nevalidan unos."
        return self.message

def konekcija():
    try:
        klijent = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        klijent.connect((socket.gethostname(), 8081))
        return klijent
    except socket.error:
        print("Greska u konekciji sa replikatorom.")
        klijent.close()
        return None

def slanje(klijent, id, potrosnja):
    try:
        podaci = pickle.dumps(podatak.Podatak(id, potrosnja))
        klijent.send(podaci)
    except socket.error:
        print("Neuspesno slanje podataka.")
        klijent.close()
        return "ERROR"

def slanje_exit(klijent, poruka_gasenja):
    try:
        podaci = pickle.dumps(poruka_gasenja)
        klijent.send(podaci)
    except socket.error:
        print("Neuspesno slanje podataka.")
        klijent.close()
    
def meni():
    
    print("Meni: \n1 - Unos potrosnje vode\n2 - Izlaz")
    odgovor = input()
    try:
        odgovor = int(odgovor)
        if odgovor <= 0 or odgovor > 2:
            raise NevalidanUnos("Unesite 1 ili 2.")
        
        return odgovor
    except NevalidanUnos as e:
        print(e)
        return None
    except Exception:
        print("Unesite broj.")
        return None
    
def unos_id_brojila():
    print("Unesite ID brojila: ")
    id_brojila = input()
    try:
        id_brojila = int(id_brojila)
        if id_brojila <= 0 or id_brojila == None:
            raise NevalidanUnos()
        
        return id_brojila
    except NevalidanUnos as e:
        print(e)
        return None
    except Exception:
        print("Unesite broj.")
        return None
    
def unos_potrosnja():
    print("Unesite potrosnju vode: ")
    id_brojila = input()
    try:
        id_brojila = int(id_brojila)
        if id_brojila <= 0 or id_brojila == None:
            raise NevalidanUnos()
        
        return id_brojila
    except NevalidanUnos as e:
        print(e)
        return None
    except Exception:
        print("Unesite broj.")
        return None
    
def main(klijent, odgovor):
            
    if odgovor == None:
        return None
    if odgovor == 1:
        id = unos_id_brojila()
        if id == None:
            return None
        
        potrosnja = unos_potrosnja()
        if potrosnja == None:
            return None
        
        if slanje(klijent, id, potrosnja) == "ERROR": 
            return None
            
        return "OK"
    elif odgovor == 2:
        slanje_exit(klijent, "EXIT")
        return "EXIT"
            
if __name__ == "__main__":
    klijent = konekcija()
    
    while True:
        odgovor = meni()
        if main(klijent, odgovor) == "EXIT":
            break
    
    klijent.close()
