class Broj_Niti:
    def __init__(self):
        self.broj_niti = 0

    def get_broj(self):
        return self.broj_niti

    def povecaj_broj(self):
        self.broj_niti += 1

    def smanji_broj(self):
        self.broj_niti -= 1