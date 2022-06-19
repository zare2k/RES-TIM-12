import socket
import pickle
import podatak
import time
        
def konekcija():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((socket.gethostname(), 8082))
        server.listen(1)
        print("Cekam konekciju...")
        soket, adresa = server.accept()
        print("Konektovan klijent sa adrese: ", adresa)
        return soket
    except socket.error:
        print("Neuspesna konekcija sa replicator sender-om")
        exit()

def konekcija_reader():
    try:
        receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        receiver.connect((socket.gethostname(), 8083))
        return receiver
    except socket.error:
        print("Neuspesna konekcija sa reader-om")
        return None
def izvlacenje_podataka(line):
    podaci_string = str.encode(line)
    podaci_niz = []
    for number in podaci_string.split():
        if number.isdigit():
            podaci_niz.append(int(number))
    podaci = podatak.Podatak(podaci_niz[0], podaci_niz[1])   
    return podaci

def slanje_reader(receiver, soket):
    try:
        file = open("log.txt", "r") 
        for line in file:
            podaci = izvlacenje_podataka(line)
            podaci_bytes = pickle.dumps(podaci)
            receiver.send(podaci_bytes)
    except Exception:
        print("Neuspesno slanje podataka na reader")
        file.close() 
        soket.close()
        receiver.close()
        return "ERROR"
    file.close() 

def primanje_podataka(soket, receiver):
    try:
        data = soket.recv(4096)
        podaci = pickle.loads(data)
        return podaci
    except EOFError:
        print("Gasenje replikator receivera.")
        soket.close()
        receiver.close()
        exit()

def logovanje(podaci):
    file = open("log.txt", "a") 
    file.write(str(podaci.id_brojila))
    file.write(" ")
    file.write(str(podaci.potrosnja_vode))
    file.write("\n")
    file.close() 

def slanje_podataka(soket, receiver):
    if slanje_reader(receiver, soket) == "ERROR":
        exit()
    brisanje_logova()
    pocetak_prikupljanja_novo = time.time()

    return pocetak_prikupljanja_novo

def brisanje_logova():
    file = open("log.txt", "a") 
    file.truncate(0)
    file.close() 

def provera_proteklog_vremena(pocetak_prikupljanja, soket, receiver):
    trenutno_vreme = time.time()
    if (trenutno_vreme - pocetak_prikupljanja) >= 10:
       pocetak_prikupljanja = slanje_podataka(soket, receiver)

    return pocetak_prikupljanja

def razmena_podataka(soket, receiver):
    pocetak_prikupljanja = time.time()
    while True:
        podaci = primanje_podataka(soket, receiver)
        logovanje(podaci)
        
        print("Podaci stigli od klijenta: ")
        print("ID brojila: ", podaci.id_brojila)
        print("Potrosnja vode: ", podaci.potrosnja_vode)

        pocetak_prikupljanja = provera_proteklog_vremena(pocetak_prikupljanja, soket, receiver)

def main():
    soket = konekcija()
    receiver = konekcija_reader()
    if receiver == None:
        return
    razmena_podataka(soket, receiver)

if __name__ == "__main__":
    main()
