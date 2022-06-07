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

def slanje_reader(receiver, podaci):
    podaci_bytes = pickle.dumps(podaci)
    receiver.send(podaci_bytes)

if __name__ == "__main__":
    
    soket = konekcija()
    receiver = konekcija_reader()
    
    lista = list()
    redni_broj = 0
    
    while True:
        podaci = pickle.loads(soket.recv(4096))
        podaci.redni_broj = redni_broj
        redni_broj += 1

        lista.append(podaci)

        print("Podaci stigli od klijenta: ")
        print("ID brojila: ", podaci.id_brojila)
        print("Potrosnja vode: ", podaci.potrosnja_vode)
        
        slanje_reader(receiver, podaci)

