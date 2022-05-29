import socket
import podatak

def konekcija():
    klijent = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    klijent.connect((socket.gethostname(), 8081))
    return klijent

if __name__ == "__main__":

    #klijent = konekcija()

    while True: 

        odgovor = input("Meni: \n1 - Unos potrosnje vode\n2 - Izlaz\n")

        if int(odgovor) == 2:
            break
        
