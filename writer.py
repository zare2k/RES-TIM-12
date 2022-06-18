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
        exit()

def slanje(klijent, id, potrosnja):
    try:
        podaci = pickle.dumps(podatak.Podatak(id, potrosnja))
        klijent.send(podaci)
    except socket.error:
        print("Neuspesno slanje podataka.")
        klijent.close()
        exit()

def slanje_exit(klijent, poruka_gasenja):
    try:
        podaci = pickle.dumps(poruka_gasenja)
        klijent.send(podaci)
    except socket.error:
        print("Neuspesno gasenje servera.")
        klijent.close()
    
def meni(odgovor):
    
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
    
def unos(odgovor):
    try:
        odgovor = int(odgovor)
        if odgovor <= 0:
            raise NevalidanUnos()
        
        return odgovor
    except NevalidanUnos as e:
        print(e)
        return None
    except Exception:
        print("Unesite broj.")
        return None
    
def main():

    klijent = konekcija()
        
    while True:
        print("Meni: \n1 - Unos potrosnje vode\n2 - Izlaz\n")
        
        odgovor = meni(input())
            
        if odgovor == None:
            continue
        if odgovor == 1:
            print("Unesite ID brojila: ")
            id = unos(input())
            print("Unesite potrosnju vode: ")
            potrosnja = unos(input())
            slanje(klijent, id, potrosnja)
            
        elif odgovor == 2:
            slanje_exit(klijent, "EXIT")
            break
            
if __name__ == "__main__":
    main()
