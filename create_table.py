import database_functions

baza = database_functions.konekcija()
myCursor = baza.cursor()

def napravi_tabelu():
  myCursor.execute("CREATE TABLE BROJILO(ID int PRIMARY KEY NOT NULL, IME VARCHAR(50) NOT NULL, PREZIME VARCHAR(50) NOT NULL, ULICA VARCHAR(50) NOT NULL, BROJ_ULICE int NOT NULL, POSTANSKI_BROJ int NOT NULL, GRAD VARCHAR(50) NOT NULL)")
  myCursor.execute("CREATE TABLE POTROSNJA_BROJILA(ID int PRIMARY KEY NOT NULL, POSTROSNJA int NOT NULL, MESEC VARCHAR(50) NOT NULL)")
  
napravi_tabelu()