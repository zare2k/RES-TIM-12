import pickle
import socket
import unittest
from unittest import mock
from podatak import Podatak
import writer
from unittest.mock import MagicMock, Mock, patch

class TestMeni(unittest.TestCase):
    
    def test_meni_ok(self):
        with mock.patch('builtins.input', return_value="1"):
            assert writer.meni() == 1
            
    def test_meni_van_opsega(self):
        with mock.patch('builtins.input', return_value="5"):
            assert writer.meni() == None
        with mock.patch('builtins.input', return_value="-3"):
            assert writer.meni() == None

    def test_meni_nije_broj(self):
        with mock.patch('builtins.input', return_value="test"):
            assert writer.meni() == None
        with mock.patch('builtins.input', return_value=[]):
            assert writer.meni() == None
            
class TestUnosId(unittest.TestCase):
    
    def test_unos_id_ok(self):
        with mock.patch('builtins.input', return_value="10"):
            assert writer.unos_id_brojila() == 10
            
    def test_unos_id_van_opsega(self):
        with mock.patch('builtins.input', return_value="-6"):
            assert writer.unos_id_brojila() == None
        with mock.patch('builtins.input', return_value=None):
            assert writer.unos_id_brojila() == None
            
    def test_id_nije_broj(self):
        with mock.patch('builtins.input', return_value="string"):
            assert writer.unos_id_brojila() == None
        with mock.patch('builtins.input', return_value=[5, 7]):
            assert writer.unos_id_brojila() == None
            
class TestUnosPotrosnja(unittest.TestCase):
    
    def test_unos_potrosnja_ok(self):
        with mock.patch('builtins.input', return_value="56"):
            assert writer.unos_potrosnja() == 56
            
    def test_unos_potrosnja_van_opsega(self):
        with mock.patch('builtins.input', return_value="-12"):
            assert writer.unos_potrosnja() == None
        with mock.patch('builtins.input', return_value=None):
            assert writer.unos_potrosnja() == None
            
    def test_potrosnja_nije_broj(self):
        with mock.patch('builtins.input', return_value="dva"):
            assert writer.unos_potrosnja() == None
        with mock.patch('builtins.input', return_value={}):
            assert writer.unos_potrosnja() == None
            
class TestSlanje(unittest.TestCase):
    @patch('writer.konekcija')
    def test_slanje_ok(self, mock_konekcija):
        mock_socket = MagicMock(socket.socket)
        mock_socket.recv = MagicMock(return_value = pickle.dumps(Podatak(1, 2)))
        mock_konekcija.return_value = mock_socket

        self.assertEqual(writer.slanje(mock_socket, 1, 2), None)
        
    @patch('writer.konekcija')
    def test_slanje_error(self, mock_konekcija):
        mock_socket = MagicMock()
        mock_socket.send.side_effect = socket.error
        mock_konekcija.returd_value = mock_socket

        self.assertEqual(writer.slanje(mock_socket, 1, 2), "ERROR")
        
    @patch('writer.konekcija')
    def test_slanje_exit_ok(self, mock_konekcija):
        mock_socket = MagicMock(socket.socket)
        mock_socket.recv = MagicMock(return_value = pickle.dumps("EXIT"))
        mock_konekcija.return_value = mock_socket

        self.assertEqual(writer.slanje_exit(mock_socket, "EXIT"), None)
                    
    @patch('writer.konekcija')
    def test_slanje_exit_error(self, mock_konekcija):
        mock_socket = MagicMock()
        mock_socket.send.side_effect = socket.error
        mock_konekcija.returd_value = mock_socket

        self.assertEqual(writer.slanje_exit(mock_socket, "EXIT"), None)
        
class TestKonekcija(unittest.TestCase):
    def test_konkecija_error(self):
        mock_socket = MagicMock()
        mock_socket.connect.side_effect = socket.error
           
        self.assertEqual(writer.konekcija(), None)
        
class TestMain(unittest.TestCase):
    @patch('writer.konekcija')
    def test_odgovor_none(self, mock_konekcija):
        mock_socket = MagicMock(socket.socket)
        mock_konekcija.return_value = mock_socket
        self.assertEqual(writer.main(mock_socket, None), None)
        
    @patch('writer.konekcija')
    @patch('writer.unos_id_brojila')
    @patch('writer.unos_potrosnja')
    @patch('writer.slanje')
    def test_odgovor_1_ok(self, mock_konekcija, mock_id_brojila, mock_potrosnja, mock_slanje):
        mock_socket = MagicMock(socket.socket)
        mock_konekcija.return_value = mock_socket
        
        mock_id = MagicMock(writer.unos_id_brojila)
        mock_id_brojila.return_value = mock_id
        
        mock_p = MagicMock(writer.unos_potrosnja)
        mock_potrosnja.return_value = mock_p
        
        mock_s = MagicMock(writer.slanje)
        mock_slanje.return_value = mock_s
        
        self.assertEqual(writer.main(mock_socket, 1), "OK")
        
    @patch('writer.konekcija')
    def test_odgovor_1_id_none(self, mock_konekcija):
        mock_socket = MagicMock(socket.socket)
        mock_konekcija.return_value = mock_socket
        
        with mock.patch('writer.unos_id_brojila', return_value=None):
            assert writer.main(mock_socket, 1) == None 
        
        
    @patch('writer.konekcija')
    @patch('writer.unos_id_brojila')
    def test_odgovor_1_potrosnja_none(self, mock_konekcija, mock_id_brojila):
        mock_socket = MagicMock(socket.socket)
        mock_konekcija.return_value = mock_socket
        
        mock_id = MagicMock(writer.unos_id_brojila)
        mock_id_brojila.return_value = mock_id
        
        with mock.patch('writer.unos_potrosnja', return_value=None):
            assert writer.main(mock_socket, 1) == None 
            
    @patch('writer.konekcija')
    @patch('writer.unos_id_brojila')
    @patch('writer.unos_potrosnja')
    def test_odgovor_1_slanje_error(self, mock_konekcija, mock_id_brojila, mock_potrosnja):
        mock_socket = MagicMock(socket.socket)
        mock_konekcija.return_value = mock_socket
        
        mock_id = MagicMock(writer.unos_id_brojila)
        mock_id_brojila.return_value = mock_id
        
        mock_p = MagicMock(writer.unos_potrosnja)
        mock_potrosnja.return_value = mock_p
        
        with mock.patch('writer.slanje', return_value="ERROR"):
            assert writer.main(mock_socket, 1) == None 
            
    @patch('writer.konekcija')
    @patch('writer.slanje_exit')
    def test_odgovor_2(self, mock_konekcija, mock_slanje_exit):
        mock_socket = MagicMock(socket.socket)
        mock_konekcija.return_value = mock_socket
        
        with mock.patch('writer.slanje', return_value=None):
            assert writer.main(mock_socket, 2) == "EXIT" 

if __name__ == "__main__":
    unittest.main()