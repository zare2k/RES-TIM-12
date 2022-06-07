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

    klijent = konekcija()

    while True: 

        odgovor = input("Meni: \n1 - Unos potrosnje vode\n2 - Izlaz\n")

        if int(odgovor) == 1:
            id = input("Unesite ID brojila: ")
            potrosnja = input("Unesite potrosnju vode: ")
            slanje(klijent, id, potrosnja)

        elif int(odgovor) == 2:
            klijent.close()
            break
        else:
            print("Niste izabrali validnu opciju!\n")
