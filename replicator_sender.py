import socket
import pickle
from _thread import *
import os
import broj_niti

def konekcija():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((socket.gethostname(), 8081))
        server.listen(5)
        print("Cekam konekciju...")
        return server
    except socket.error:
        print("Neuspesna konekcija sa writer-om")
        exit()

def konekcija_receiver():
    try:
        klijent = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        klijent.connect((socket.gethostname(), 8082))
        return klijent
    except socket.error:
        print("Neuspesna konekcija sa replicator receiver-om")
        exit()
    
def slanje_receiver(klijent, podaci):
    try:
        podaci_bytes = pickle.dumps(podaci)
        klijent.send(podaci_bytes)
    except socket.error:
        print("Neuspesno slanje podataka na replicator receiver")
        exit()

def primanje_podataka(soket):
    try:
        data = soket.recv(4096)
        if not data:
            return None
        podaci = pickle.loads(data)
        return podaci
    except Exception:
        return None

def gasenje_servera(gasenje, soket, klijent):
    if gasenje == "DA":
        print("Gasi se replikator sender.")
        soket.close()
        klijent.close()
        os._exit(1)

def gasenje_klijenta(podaci, soket, klijent, broj_niti):
    if podaci == "EXIT":
        broj_niti.smanji_broj()
        if broj_niti.get_broj() == 0:
            gasenje = input("Svi klijenti su ugaseni. Unesite DA za gasenje servera: ")
            gasenje_servera(gasenje, soket, klijent)

def visestruka_konekcija(soket, klijent, broj_niti):
    while True:
        podaci = primanje_podataka(soket)
        if podaci == None:
            break

        gasenje_klijenta(podaci, soket, klijent, broj_niti)
        
        print("Podaci stigli od klijenta: ")
        print("ID brojila: ", podaci.id_brojila)
        print("Potrosnja vode: ", podaci.potrosnja_vode) 

        slanje_receiver(klijent, podaci)
    soket.close()

def razmena_podataka(server, klijent):
    broj_niti_replikator = broj_niti.Broj_Niti()
    while True:
        soket, adresa = server.accept()
        print("Konektovan klijent sa adrese: ", adresa) 

        start_new_thread(visestruka_konekcija, (soket, klijent, broj_niti_replikator))
        broj_niti_replikator.povecaj_broj()

def main():
    server = konekcija()
    klijent = konekcija_receiver()

    razmena_podataka(server, klijent)
        
if __name__ == "__main__":
    main()
