import socket
import pickle
import database_functions
import random

def konekcija():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((socket.gethostname(), 8083))
        server.listen(1)
        print("Cekam konekciju...")
        soket, adresa = server.accept()
        print("Konektovan klijent sa adrese: ", adresa)
        return soket
    except socket.error:
        print("Neuspesna konekcija sa replicator receiver-om")
        exit()

def preuzimanje_podataka(soket):
    try:
        data = soket.recv(4096)
        podaci = pickle.loads(data)
        return podaci
    except EOFError:
        print("Ugasen replikator, gasenje readera.")
        soket.close()
        return None
    except ConnectionResetError:
        return None

def upis_u_bazu(niz_meseci, podaci, baza):
    rezultat = database_functions.provera_id(podaci.id_brojila, baza)
    if len(rezultat) == 0:
        print("Nemoguce dodavanje. Ne postoji id u tabeli.")
        return
    mesec = random.choice(niz_meseci)
    rezultat = database_functions.provera_mesec(podaci.id_brojila, mesec, baza)
    if len(rezultat) != 0:
        print("Nemoguce dodavanje. Vec je unet mesec za dato brojilo")
        return
    database_functions.dodaj_element(podaci.id_brojila, podaci.potrosnja_vode, mesec, baza)

def main():
    soket = konekcija()
    baza = database_functions.konekcija()
    niz_meseci = ['Januar', 'Februar', 'Mart', 'April', 'Maj', 'Jun', 'Jul', 'Avgust', 'Septembar', 'Oktobar', 'Novembar', 'Decembar']
    while True:
        podaci = preuzimanje_podataka(soket)
        if podaci == None:
            break
        print("Podaci stigli od klijenta: ")
        print("ID brojila: ", podaci.id_brojila)
        print("Potrosnja vode: ", podaci.potrosnja_vode)
        upis_u_bazu(niz_meseci, podaci, baza)
    
if __name__ == "__main__":
    main()
