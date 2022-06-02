import socket
import pickle
import podatak
        
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

def slanje_reader(receiver, id, potrosnja):
    podaci = pickle.dumps(podatak.Podatak(id, potrosnja))
    receiver.send(podaci)

if __name__ == "__main__":
    
    soket = konekcija()
    receiver = konekcija_reader()
    
    lista = list()
    redni_broj = 0
    
    while True:
        podaci = pickle.loads(soket.recv(4096))
        
        lista.append((podaci, redni_broj))
        redni_broj += 1
        
        print("Podaci stigli od klijenta: ")
        print("ID brojila: ", podaci.idBrojila)
        print("Potrosnja vode: ", podaci.potrosnjaVode)
        
        slanje_reader(receiver, podaci.idBrojila, podaci.potrosnjaVode)
