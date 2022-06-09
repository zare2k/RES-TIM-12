import socket
import pickle
import podatak
import time
        
def konekcija():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 8082))
    s.listen(1)
    print("Cekam konekciju...")
    soket, adresa = s.accept()
    print("Konektovan klijent sa adrese: ", adresa)
    return soket

def konekcija_reader():
    receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver.connect((socket.gethostname(), 8083))
    return receiver

def slanje_reader(receiver, lista):
    podaci_bytes = pickle.dumps(lista)
    receiver.send(podaci_bytes)

if __name__ == "__main__":
    
    try:
        soket = konekcija()
    except socket.error:
        print("Greska u konekciji sa replikator senderom.")
        exit(1)
    try:
        receiver = konekcija_reader()
    except socket.error:
        print("Greska u konekciji sa reader-om.")
        exit(1)
    
    lista = list()
    pocetak_prikupljanja = time.time()

    while True:
        try:
            podaci = pickle.loads(soket.recv(4096))
            lista.append(podaci)
        except EOFError:
            odgovor = input("Ugasen klijent, da li zelite da ugasite server? (DA/NE)")
            if odgovor == "NE":
                soket = konekcija()
                continue
            elif odgovor == "DA":
                soket.close()
                receiver.close()
                break
            else:
                print("Unesite DA ili NE")
                continue

        print("Podaci stigli od klijenta: ")
        print("ID brojila: ", podaci.id_brojila)
        print("Potrosnja vode: ", podaci.potrosnja_vode)

        trenutno_vreme = time.time()
        if (trenutno_vreme - pocetak_prikupljanja) >= 10:
            try:
                slanje_reader(receiver, lista)
                lista.clear()
                print("Duzina liste: ", str(len(lista)))
                pocetak_prikupljanja = time.time()
            except socket.error:
                print("Neuspesno slanje podataka reader komponenti.")
                soket.close()
                receiver.close()
                exit(1)
