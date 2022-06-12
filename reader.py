import socket
import pickle
import database_functions
import random

def konekcija():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 8083))
    s.listen(1)
    print("Cekam konekciju...")
    soket, adresa = s.accept()
    print("Konektovan klijent sa adrese: ", adresa)
    return soket

if __name__ == "__main__":
    
    try:
        soket = konekcija()
    except socket.error:
        print("Greska u konekciji sa replikatorom.")
        exit(1)

    baza = database_functions.konekcija()
    niz_meseci = ['Januar', 'Februar', 'Mart', 'April', 'Maj', 'Jun', 'Jul', 'Avgust', 'Septembar', 'Oktobar', 'Novembar', 'Decembar']
    
    while True:
        try:
            podaci = pickle.loads(soket.recv(4096))
        except EOFError:
            odgovor = input("Ugasen klijent, da li zelite da ugasite server? (DA/NE)")
            if odgovor == "NE":
                soket = konekcija()
                continue
            elif odgovor == "DA":
                soket.close()
                break
            else:
                print("Unesite DA ili NE")
                continue

        print("Podaci stigli od klijenta: ")
        for i in range(len(podaci)):
            print("ID brojila: ", podaci[i].id_brojila)
            print("Potrosnja vode: ", podaci[i].potrosnja_vode)
            mesec = random.choice(niz_meseci)
            database_functions.dodaj_element(podaci[i].id_brojila, podaci[i].potrosnja_vode, mesec, baza)

