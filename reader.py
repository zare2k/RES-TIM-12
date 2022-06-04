import socket
import pickle
import podatak
import database_functions

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
    baza = database_functions.konekcija()

    while True:
        podaci = pickle.loads(soket.recv(4096))

        print("Podaci stigli od klijenta: ")
        print("ID brojila: ", podaci.id_brojila)
        print("Potrosnja vode: ", podaci.potrosnja_vode)
        #database_functions.dodaj_element(podaci.id_brojila, podaci.potrosnja_vode, baza)
