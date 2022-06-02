import socket
import pickle
import podatak

def konekcija():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 8081))
    s.listen(5)
    print("Cekam konekciju...")
    soket, adresa = s.accept()
    print("Konektovan klijent sa adrese: ", adresa)
    return soket

def konekcija_receiver():
    klijent = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    klijent.connect((socket.gethostname(), 8082))
    return klijent
    
def slanje_receiver(klijent, podaci):
    podaci_bytes = pickle.dumps(podaci)
    klijent.send(podaci_bytes)

if __name__ == "__main__":
    
    soket = konekcija()
    klijent = konekcija_receiver()
    
    while True:
        podaci = pickle.loads(soket.recv(4096))
        print("Podaci stigli od klijenta: ")
        print("ID brojila: ", podaci.id_brojila)
        print("Potrosnja vode: ", podaci.potrosnja_vode)
        
        slanje_receiver(klijent, podaci)
        
