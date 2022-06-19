import pickle
import socket
import unittest
from broj_niti import Broj_Niti
from podatak import Podatak
import replicator_sender
from unittest.mock import MagicMock, patch

class TestSlanje(unittest.TestCase):
    @patch('replicator_sender.konekcija')
    def test_slanje_receiver_ok(self, mock_konekcija):
        mock_socket = MagicMock(socket.socket)
        mock_socket.recv = MagicMock(return_value = pickle.dumps(Podatak(1, 2)))
        mock_konekcija.return_value = mock_socket

        self.assertEqual(None, replicator_sender.slanje_receiver(mock_socket, Podatak(1, 2)))

    @patch('replicator_sender.konekcija')
    def test_slanje_receiver_error(self, mock_konekcija):
        mock_socket = MagicMock()
        mock_socket.send.side_effect = socket.error
        mock_konekcija.return_value = mock_socket

        self.assertEqual("ERROR", replicator_sender.slanje_receiver(mock_socket, Podatak(1, 2)))

class TestKonekcijaReceiver(unittest.TestCase):
    @patch('replicator_sender.konekcija')
    def test_konekcija_receiver_ok(self, mock_konekcija):
        mock_socket = MagicMock(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        mock_socket.connect = MagicMock(mock_socket.connect((socket.gethostname(), 8082)))
        mock_konekcija.return_value = mock_socket.connect

        self.assertEqual(None, replicator_sender.konekcija_receiver())


class TestKonekcija(unittest.TestCase):
    @patch('replicator_sender.konekcija')
    def test_konekcija_ok(self, mock_socket_finish):
        mock_socket = MagicMock(socket.socket)
        mock_socket.bind = MagicMock(mock_socket.bind((socket.gethostname(), 8081)))
        mock_socket.listen = MagicMock(mock_socket.listen(5))
        mock_socket_finish.return_value = mock_socket.listen

        self.assertEqual(mock_socket.listen, replicator_sender.konekcija())

class TestGasenjeServera(unittest.TestCase):
    @patch('replicator_sender.socket')
    @patch('replicator_sender.socket')
    def test_gasenje_servera_ok(self, mock_socket_1, mock_socket_2):
        mock_gasenje = "DA"
        mock_socket_server = MagicMock(socket.socket)
        mock_socket_klijent = MagicMock(socket.socket)
        mock_socket_1.return_value = mock_socket_server
        mock_socket_2.return_value = mock_socket_klijent

        self.assertEqual("EXIT", replicator_sender.gasenje_servera(mock_gasenje, mock_socket_1, mock_socket_2))

class TestGasenjeKlijenta(unittest.TestCase):
    @patch('replicator_sender.socket')
    @patch('replicator_sender.socket')
    def test_gasenje_servera_ok(self, mock_socket_1, mock_socket_2):
        mock_gasenje = "EXIT"
        broj_niti = Broj_Niti()
        broj_niti.povecaj_broj()
        mock_socket_server = MagicMock(socket.socket)
        mock_socket_klijent = MagicMock(socket.socket)
        mock_socket_1.return_value = mock_socket_server
        mock_socket_2.return_value = mock_socket_klijent

        self.assertEqual(None, replicator_sender.gasenje_klijenta(mock_gasenje, mock_socket_1, mock_socket_2, broj_niti))

class TestVisestrukaKonekcija(unittest.TestCase):
    @patch('replicator_sender.socket')
    @patch('replicator_sender.socket')
    def test_visestruka_konekcija_ok(self, mock_socket_1, mock_socket_2):
        broj_niti = Broj_Niti()
        broj_niti.povecaj_broj()
        mock_socket_server = MagicMock(socket.socket)
        mock_socket_klijent = MagicMock(socket.socket)
        mock_socket_1.return_value = mock_socket_server
        mock_socket_2.return_value = mock_socket_klijent

        self.assertEqual(None, replicator_sender.visestruka_konekcija(mock_socket_1, mock_socket_2, broj_niti))

class TestMain(unittest.TestCase):
    def test_main_ok(self):

        self.assertEqual(None, replicator_sender.main())


if __name__ == "__main__":
    unittest.main()