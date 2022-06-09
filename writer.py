import socket
import podatak
import pickle

def konekcija():
    klijent = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    klijent.connect((socket.gethostname(), 8081))
    return klijent

def slanje(klijent, id, potrosnja):
    podaci = pickle.dumps(podatak.Podatak(id, potrosnja))
    klijent.send(podaci)

if __name__ == "__main__":

    try:
        klijent = konekcija()
    except socket.error:
        print("Greska u konekciji sa replikatorom.")
        exit(1)
    
    while True: 

        odgovor = input("Meni: \n1 - Unos potrosnje vode\n2 - Izlaz\n")
        
        try:
            odgovor = int(odgovor)
        except ValueError:
            print("Unesite broj")
            continue
        
        if odgovor == 1:
            
            try:
                id = int(input("Unesite ID brojila: "))
            except ValueError:
                print("ID mora biti broj")
                continue
            
            try:
                potrosnja = int(input("Unesite potrosnju vode: "))
            except ValueError:
                print("Morate uneti broj")
                continue
            
            try:
                slanje(klijent, id, potrosnja)
            except socket.error:
                print("Neuspesno slanje podataka.")
                klijent.close()
                exit(1)
                
        elif odgovor == 2:
            klijent.close()
            break
        else:
            print("Niste izabrali validnu opciju!\n")
