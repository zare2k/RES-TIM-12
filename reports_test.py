from decimal import Decimal
from tkinter.messagebox import NO
import unittest
from unittest import mock
from podatak import Podatak
import reports
from unittest.mock import MagicMock, Mock, patch
import database_functions
import mysql.connector

class TestMeni(unittest.TestCase):
    
    def test_meni_ok(self):
        with mock.patch('builtins.input', return_value="2"):
            assert reports.meni() == 2
            
    def test_meni_van_opsega(self):
        with mock.patch('builtins.input', return_value="23"):
            assert reports.meni() == None
        with mock.patch('builtins.input', return_value="-12"):
            assert reports.meni() == None

    def test_meni_nije_broj(self):
        with mock.patch('builtins.input', return_value="test"):
            assert reports.meni() == None
        with mock.patch('builtins.input', return_value=[]):
            assert reports.meni() == None
            
class TestUnosUlica(unittest.TestCase):
    
    def test_unos_ulica_ok(self):
        with mock.patch('builtins.input', return_value="Kosovska"):
            assert reports.unos_ulica() == "Kosovska"
            
    def test_unos_ulica_broj(self):
        with mock.patch('builtins.input', return_value="6543"):
            assert reports.unos_ulica() == None
        with mock.patch('builtins.input', return_value="234"):
            assert reports.unos_ulica() == None
            
class TestUnosBrojilo(unittest.TestCase):
    
    def test_unos_brojilo_ok(self):
        with mock.patch('builtins.input', return_value="2"):
            assert reports.unos_brojilo() == 2
            
    def test_unos_brojilo_error(self):
        with mock.patch('builtins.input', return_value="-23"):
            assert reports.unos_brojilo() == None
        with mock.patch('builtins.input', return_value="test"):
            assert reports.unos_brojilo() == None
            
class TestMain(unittest.TestCase):
    
    @patch('database_functions.konekcija')
    @patch('reports.izvestaj')
    def test_main_ok(self, mock_konekcija, mock_izvestaj):
        
        mock_kon = MagicMock(mysql.connector.connect)
        mock_konekcija.return_value = mock_kon
        
        mock_i = MagicMock(reports.izvestaj)
        mock_izvestaj.return_value = mock_i
        
        self.assertEqual(reports.main(mock_konekcija, None), None)
        self.assertEqual(reports.main(mock_konekcija, 3), "EXIT")
        
        with mock.patch('reports.izvestaj', return_value=None):
            assert reports.main(mock_konekcija, 2) == None
            
class TestIspisIzvestaj(unittest.TestCase):
    def test_ispis_izvestaj_ok(self):
        rezultat = ["123", "Januar"]
        self.assertEqual(reports.izvestaj_ispis(rezultat), "OK")
        
    def test_ispis_izvestaj_error(self):
        rezultat = None
        self.assertEqual(reports.izvestaj_ispis(rezultat), "ERROR")
        
class TestIzvestaj(unittest.TestCase):
    @patch('database_functions.konekcija')
    def test_izvestaj_1_ulica_none(self, mock_konekcija):
        
        mock_kon = MagicMock(mysql.connector.connect)
        mock_konekcija.return_value = mock_kon
        
        with mock.patch('reports.unos_ulica', return_value=None):
            assert reports.izvestaj(1, mock_konekcija) == None
            
    @patch('database_functions.konekcija')
    @patch('reports.izvestaj_ulica')
    @patch('reports.izvestaj_ispis')
    @patch('reports.unos_ulica')
    def test_izvestaj_ulica_ok(self, mock_konekcija, mock_izvestaj_ulica, mock_izvestaj_ispis, mock_ulica):
        mock_kon = MagicMock(mysql.connector.connect)
        mock_konekcija.return_value = mock_kon
        
        mock_u = MagicMock(reports.unos_ulica)
        mock_ulica.return_value = mock_u
        
        mock_i_u = MagicMock(reports.izvestaj_ulica)
        mock_izvestaj_ulica.return_value = mock_i_u
        
        mock_i_i = MagicMock(reports.izvestaj_ispis)
        mock_izvestaj_ispis.return_value = mock_i_i
        
        with mock.patch('reports.duzina_liste', return_value=3):
            assert reports.izvestaj(1, mock_konekcija) == "OK"
            
    @patch('database_functions.konekcija')
    @patch('reports.izvestaj_ulica')
    @patch('reports.unos_ulica')
    def test_izvestaj_ulica_ne_postoji(self, mock_konekcija, mock_izvestaj_ulica, mock_ulica):
        mock_kon = MagicMock(mysql.connector.connect)
        mock_konekcija.return_value = mock_kon
        
        mock_u = MagicMock(reports.unos_ulica)
        mock_ulica.return_value = mock_u
        
        mock_i_u = MagicMock(reports.izvestaj_ulica)
        mock_izvestaj_ulica.return_value = mock_i_u
        
        with mock.patch('reports.duzina_liste', return_value=0):
            assert reports.izvestaj(1, mock_konekcija) == None
        
        
    @patch('database_functions.konekcija')
    @patch('reports.unos_ulica')
    def test_izvestaj_brojilo_none(self, mock_konekcija, mock_ulica):
        
        mock_kon = MagicMock(mysql.connector.connect)
        mock_konekcija.return_value = mock_kon
        
        mock_u = MagicMock(reports.unos_ulica)
        mock_ulica.return_value = mock_u
        
        with mock.patch('reports.unos_brojilo', return_value=None):
            assert reports.izvestaj(2, mock_konekcija) == None
            
    @patch('database_functions.konekcija')
    @patch('reports.izvestaj_brojilo')
    @patch('reports.izvestaj_ispis')
    @patch('reports.unos_brojilo')
    def test_izvestaj_brojilo_ok(self, mock_konekcija, mock_izvestaj_brojilo, mock_izvestaj_ispis, mock_brojilo):
        mock_kon = MagicMock(mysql.connector.connect)
        mock_konekcija.return_value = mock_kon
        
        mock_b = MagicMock(reports.unos_brojilo)
        mock_brojilo.return_value = mock_b
        
        mock_i_b = MagicMock(reports.izvestaj_brojilo)
        mock_izvestaj_brojilo.return_value = mock_i_b
        
        mock_i_i = MagicMock(reports.izvestaj_ispis)
        mock_izvestaj_ispis.return_value = mock_i_i
        
        with mock.patch('reports.duzina_liste', return_value=3):
            assert reports.izvestaj(2, mock_konekcija) == "OK"
            
    @patch('database_functions.konekcija')
    @patch('reports.izvestaj_brojilo')
    @patch('reports.unos_brojilo')
    def test_izvestaj_brojilo_ne_postoji(self, mock_konekcija, mock_izvestaj_brojilo, mock_brojilo):
        mock_kon = MagicMock(mysql.connector.connect)
        mock_konekcija.return_value = mock_kon
        
        mock_b = MagicMock(reports.unos_brojilo)
        mock_brojilo.return_value = mock_b
        
        mock_i_b = MagicMock(reports.izvestaj_brojilo)
        mock_izvestaj_brojilo.return_value = mock_i_b
        
        with mock.patch('reports.duzina_liste', return_value=0):
            assert reports.izvestaj(2, mock_konekcija) == None
            
class TestIzvestajUlica(unittest.TestCase):
    def test_izvestaj_ulica_ok(self):
        baza = database_functions.konekcija()
        rezultat = [('Kosovska', Decimal('10'), 'Mart'),
                    ('Kosovska', Decimal('120'), 'Septembar'),
                    ('Kosovska', Decimal('30'), 'April'),
                    ('Kosovska', Decimal('20'), 'Oktobar'),
                    ('Kosovska', Decimal('30'), 'Januar'),
                    ('Kosovska', Decimal('5'), 'Avgust')]
        self.assertEqual(reports.izvestaj_ulica("Kosovska", baza), rezultat)
        
    def test_izvestaj_ulica_error(self):
        baza = database_functions.konekcija()
        self.assertEqual(reports.izvestaj_ulica("test", baza), [])
        
class TestIzvestajBrojilo(unittest.TestCase):
    def test_izvestaj_brojilo_ok(self):
        baza = database_functions.konekcija()
        rezultat = [(2, 10, 'Mart'),
                    (2, 20, 'Oktobar'),
                    (2, 30, 'Januar'),
                    (2, 100, 'Septembar'),
                    (2, 5, 'Avgust')]
        self.assertEqual(reports.izvestaj_brojilo(2, baza), rezultat)
        
    def test_izvestaj_brojilo_error(self):
        baza = database_functions.konekcija()
        self.assertEqual(reports.izvestaj_brojilo(56, baza), [])
        
if __name__ == "__main__":
    unittest.main()