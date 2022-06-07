import database_functions

baza = database_functions.konekcija()
myCursor = baza.cursor()

myCursor.execute("CREATE TABLE BROJILO(ID int PRIMARY KEY NOT NULL AUTO_INCREMENT, IME VARCHAR(50) NOT NULL, PREZIME VARCHAR(50) NOT NULL, ULICA VARCHAR(50) NOT NULL, BROJ_ULICE int NOT NULL, POSTANSKI_BROJ int NOT NULL, GRAD VARCHAR(50) NOT NULL)")
myCursor.execute("CREATE TABLE POTROSNJA_BROJILA(REDNI_BROJ int PRIMARY KEY NOT NULL AUTO_INCREMENT, ID int NOT NULL, POTROSNJA int NOT NULL, MESEC VARCHAR(50) NOT NULL)")
  
myCursor.execute("INSERT INTO brojilo(id, ime, prezime, ulica, broj_ulice, postanski_broj, grad) VALUES ('1', 'Marko', 'Markovic', 'Sindjeliceva', '45', '15000', 'Sabac')")
myCursor.execute("INSERT INTO brojilo (id, ime, prezime, ulica, broj_ulice, postanski_broj, grad) VALUES ('2', 'Petar', 'Petrovic', 'Kosovska', '105', '21000', 'Novi Sad')")
myCursor.execute("INSERT INTO brojilo (id, ime, prezime, ulica, broj_ulice, postanski_broj, grad) VALUES ('3', 'Jovan', 'Jovanovic', 'Nemanjina', '12', '11000', 'Beograd')")
myCursor.execute("INSERT INTO brojilo (id, ime, prezime, ulica, broj_ulice, postanski_broj, grad) VALUES ('4', 'Jelena', 'Jankovic', 'Zrenjaninova', '117', '21460', 'Vrbas')")
myCursor.execute("INSERT INTO brojilo (id, ime, prezime, ulica, broj_ulice, postanski_broj, grad) VALUES ('5', 'Marijana', 'Stevanovic', 'Kolubarska', '123', '32000', 'Cacak')")
myCursor.execute("INSERT INTO brojilo (id, ime, prezime, ulica, broj_ulice, postanski_broj, grad) VALUES ('6', 'Marija', 'Milovanovic', 'Cerska', '21', '15000', 'Sabac')")
myCursor.execute("INSERT INTO brojilo (id, ime, prezime, ulica, broj_ulice, postanski_broj, grad) VALUES ('7', 'Stefan', 'Micic', 'Ruzveltova', '76', '35000', 'Jagodina')")
myCursor.execute("INSERT INTO brojilo (id, ime, prezime, ulica, broj_ulice, postanski_broj, grad) VALUES ('8', 'Maksim', 'Lazic', 'Dositejeva', '90', '18000', 'Nis')")
myCursor.execute("INSERT INTO brojilo (id, ime, prezime, ulica, broj_ulice, postanski_broj, grad) VALUES ('9', 'Milica', 'Pijunovic', 'Zanatlijska', '3', '22400', 'Ruma')")
myCursor.execute("INSERT INTO brojilo (id, ime, prezime, ulica, broj_ulice, postanski_broj, grad) VALUES ('10', 'Iskra', 'Mihajlovic', 'Norveska', '14', '24000', 'Subotica')") 
baza.commit()
