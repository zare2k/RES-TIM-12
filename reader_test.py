import socket
import unittest
from podatak import Podatak
import reader
from unittest.mock import MagicMock, patch
import database_functions

class TestiranjeUpisa(unittest.TestCase):
    @patch('database_functions.konekcija')
    def test_upis_u_bazu(self, mock_baza):
        test_meseci = ['Januar', 'Februar', 'Mart', 'April', 'Maj', 'Jun', 'Jul', 'Avgust', 'Septembar', 'Oktobar', 'Novembar', 'Decembar']
        test_podaci = Podatak(1, 2)
        mock_baza = database_functions.konekcija()

        self.assertEqual(None, reader.upis_u_bazu(test_meseci, test_podaci, mock_baza))

class TestiranjePreuzimanjePodataka(unittest.TestCase):
    @patch('socket.socket.recv', new_callable=mock_open)
    def test_main_ok(self, mock_socket):
        mock_socket = MagicMock(socket.socket)
        mock_socket.recv = MagicMock(socket.socket.recv)

        self.assertRaises(Exception, reader.preuzimanje_podataka(mock_socket))

class TestiranjeMain(unittest.TestCase):
    def test_main_ok(self):
        self.assertNotEqual(None, reader.main())

if __name__ == "__main__":
    unittest.main()