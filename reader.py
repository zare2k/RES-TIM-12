import socket
        
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