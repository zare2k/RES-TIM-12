import socket
import pickle
import podatak

def konekcija():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 8083))
    s.listen(1)
    print("Cekam konekciju...")
    soket, adresa = s.accept()
    print("Konektovan klijent sa adrese: ", adresa)
    return soket

if __name__ == "__main__":
    
    soket = konekcija()

    while True:
        podaci = pickle.loads(soket.recv(4096))

        print("Podaci stigli od klijenta: ")
        print("ID brojila: ", podaci.id_brojila)
        print("Potrosnja vode: ", podaci.potrosnja_vode)
