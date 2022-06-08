import socket
import pickle
from _thread import *

def visestruka_konekcija(konekcija, klijent):
    while True:
        data = konekcija.recv(4096)
        if not data:
            break
        podaci = pickle.loads(data)
        print("Podaci stigli od klijenta: ")
        print("ID brojila: ", podaci.id_brojila)
        print("Potrosnja vode: ", podaci.potrosnja_vode)
        
        slanje_receiver(klijent, podaci)
    konekcija.close()

def konekcija():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 8081))
    s.listen(5)
    print("Cekam konekciju...")
    return s

def konekcija_receiver():
    klijent = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    klijent.connect((socket.gethostname(), 8082))
    return klijent
    
def slanje_receiver(klijent, podaci):
    podaci_bytes = pickle.dumps(podaci)
    klijent.send(podaci_bytes)

if __name__ == "__main__":
    
    s = konekcija()
    klijent = konekcija_receiver()
    
    while True:
        soket, adresa = s.accept()
        print("Konektovan klijent sa adrese: ", adresa)
        
        start_new_thread(visestruka_konekcija, (soket, klijent))
        
