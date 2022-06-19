import pickle
import socket
import unittest
from podatak import Podatak
import replicator_receiver
from unittest.mock import MagicMock, patch

class TestKonekcijaReader(unittest.TestCase):
    @patch('replicator_receiver.konekcija')
    def test_konekcija_reader_ok(self, mock_konekcija):
        mock_socket = MagicMock(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        mock_socket.connect = MagicMock(mock_socket.connect((socket.gethostname(), 8082)))
        mock_konekcija.return_value = mock_socket.connect 

        self.assertEqual(None, replicator_receiver.konekcija_reader())

class TestIzvlacenjePodataka(unittest.TestCase):
    def test_izvlacenje_podataka_ok(self):
        mock_podaci_string = "1 2"
        rezultat = Podatak(1, 2)

        self.assertNotEqual(rezultat, replicator_receiver.izvlacenje_podataka(mock_podaci_string))

class TestLogovanje(unittest.TestCase):
    def test_logovanje_ok(self):
        rezultat = Podatak(1, 2)

        self.assertEqual(None, replicator_receiver.logovanje(rezultat))

    def test_brisanje_logova_ok(self):
        self.assertEqual(None, replicator_receiver.brisanje_logova())

class TestSlanjeReader(unittest.TestCase):
    @patch('replicator_sender.socket')
    @patch('replicator_sender.socket')
    def test_slanje_reader_ok(self, mock_socket_1, mock_socket_2):
        mock_socket_server = MagicMock(socket.socket)
        mock_socket_klijent = MagicMock(socket.socket)
        mock_socket_1.return_value = mock_socket_server
        mock_socket_2.return_value = mock_socket_klijent

        self.assertEqual(None, replicator_receiver.slanje_reader( mock_socket_1, mock_socket_2))

    @patch('replicator_sender.socket')
    def test_slanje_reader_error(self, mock_socket_2):
        mock_socket_server = socket.socket
        mock_socket_klijent = MagicMock(socket.socket)
        mock_socket_2.return_value = mock_socket_klijent

        self.assertRaises(Exception, replicator_receiver.slanje_reader, mock_socket_server, mock_socket_2)

class TestRazmenaPodataka(unittest.TestCase):
    @patch('replicator_sender.socket')
    @patch('replicator_sender.socket')
    def test_razmena_podataka_ok(self, mock_socket_1, mock_socket_2):
        mock_socket_server = MagicMock(socket.socket.recv)
        mock_socket_klijent = MagicMock(socket.socket)
        mock_socket_1.return_value = mock_socket_server
        mock_socket_2.return_value = mock_socket_klijent

        self.assertEqual(None, replicator_receiver.razmena_podataka(mock_socket_1, mock_socket_2))


if __name__ == "__main__":
    unittest.main()