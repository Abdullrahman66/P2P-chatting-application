import unittest
from unittest.mock import MagicMock, patch
from peer import peerMain
from peer import PeerClient
from peer import PeerServer  




class Testpeer(unittest.TestCase):
    def setUp(self):
        # Create an instance of YourClass with mock sockets
        self.peer_main_instance = peerMain()
        self.peer_main_instance.tcpClientSocket = MagicMock()
        self.peer_main_instance.udpClientSocket = MagicMock()

    def tearDown(self):
        # Cleanup any resources if needed
        pass

    def test_create_account(self):
        # Test createAccount function
        # Mock the send and recv methods to simulate responses
        self.peer_main_instance.tcpClientSocket.recv.return_value = "join-success"
        with unittest.mock.patch('builtins.input', return_value='Mariam mariam123'):
            self.peer_main_instance.createAccount("Mariam", "mariam123")
        # Assert that the correct message is sent and the correct print statement is executed
        self.peer_main_instance.tcpClientSocket.send.assert_called_with("JOIN Mariam mariam123".encode())
        self.assertEqual(self.peer_main_instance.tcpClientSocket.recv.call_count, 1)
        self.assertEqual(self.peer_main_instance.tcpClientSocket.recv.return_value, "join-success")
        self.assertEqual(self.peer_main_instance.createAccount("Mariam", "mariam123"), None)




    def test_login(self):
        # Test login function
        self.peer_main_instance.tcpClientSocket.recv.return_value = "login-success"
        result = self.peer_main_instance.login("Abdelrahman", "abdelrahman123", 1234)
        self.assertEqual(result, 1)
        self.peer_main_instance.tcpClientSocket.send.assert_called_with("LOGIN Abdelrahman abdelrahman123 1234".encode())
        self.assertEqual(self.peer_main_instance.tcpClientSocket.recv.call_count, 1)
        self.assertEqual(self.peer_main_instance.tcpClientSocket.recv.return_value, "login-success")

    def test_logout(self):
        # Test logout function
        self.peer_main_instance.logout(1)
        self.peer_main_instance.tcpClientSocket.send.assert_called_with("LOGOUT Abdelrahman".encode())

    def test_get_online_peers(self):
        # Test getOnlinePeers function
        self.peer_main_instance.tcpClientSocket.recv.return_value = "peer1 peer2 peer3"
        result = self.peer_main_instance.getOnlinePeers()
        self.assertEqual(result, "Online Peers: peer1 peer2 peer3")
        self.peer_main_instance.tcpClientSocket.send.assert_called_with("ONLINE online".encode())
        self.assertEqual(self.peer_main_instance.tcpClientSocket.recv.call_count, 1)
        self.assertEqual(self.peer_main_instance.tcpClientSocket.recv.return_value, "peer1 peer2 peer3")

    def test_create_chatroom(self):
        # Test createChatroom function
        self.peer_main_instance.tcpClientSocket.recv.return_value = "create-room-success"
        self.peer_main_instance.createChatroom("Networks", "Abdelrahman")
        self.peer_main_instance.tcpClientSocket.send.assert_called_with("CREATE_ROOM Networks Abdelrahman".encode())
        self.assertEqual(self.peer_main_instance.tcpClientSocket.recv.call_count, 1)
        self.assertEqual(self.peer_main_instance.tcpClientSocket.recv.return_value, "create-room-success")

    def test_join_chatroom(self):
        # Test joinchatRoom function
        self.peer_main_instance.tcpClientSocket.recv.return_value = "join-room-success"
        self.peer_main_instance.joinchatRoom("Networks", "Abdelrahman")
        self.peer_main_instance.tcpClientSocket.send.assert_called_with("JOIN_ROOM Networks Abdelrahman".encode())
        self.assertEqual(self.peer_main_instance.tcpClientSocket.recv.call_count, 1)
        self.assertEqual(self.peer_main_instance.tcpClientSocket.recv.return_value, "join-room-success")

    def test_list_chatrooms(self):
        # Test list_Chatrooms function
        self.peer_main_instance.tcpClientSocket.recv.return_value = "room1:room2:room3"
        result = self.peer_main_instance.list_Chatrooms("RoomName")
        self.assertEqual(result, ["room1", "room2", "room3"])
        self.peer_main_instance.tcpClientSocket.send.assert_called_with("get_users Networks".encode())
        self.assertEqual(self.peer_main_instance.tcpClientSocket.recv.call_count, 1)
        self.assertEqual(self.peer_main_instance.tcpClientSocket.recv.return_value, "room1:room2:room3")

    def test_search_user(self):
        # Test searchUser function
        self.peer_main_instance.tcpClientSocket.recv.return_value = "search-success Mariam"
        result = self.peer_main_instance.searchUser("Mariam")
        self.assertEqual(result, "Mariam")
        self.peer_main_instance.tcpClientSocket.send.assert_called_with("SEARCH Mariam".encode())
        self.assertEqual(self.peer_main_instance.tcpClientSocket.recv.call_count, 1)
        self.assertEqual(self.peer_main_instance.tcpClientSocket.recv.return_value, "search-success Mariam")

    def test_search_users(self):
        # Test search_users function
        self.peer_main_instance.tcpClientSocket.recv.return_value = "search-success Mariam"
        result = self.peer_main_instance.search_users("Mariam")
        self.assertEqual(result, "Mariam")
        self.peer_main_instance.tcpClientSocket.send.assert_called_with("SEARCH Mariam".encode())
        self.assertEqual(self.peer_main_instance.tcpClientSocket.recv.call_count, 1)
        self.assertEqual(self.peer_main_instance.tcpClientSocket.recv.return_value, "search-success Mariam")

    def test_send_hello_message(self):
        # Test sendHelloMessage function
        self.peer_main_instance.udpClientSocket.sendto.return_value = None
        self.peer_main_instance.sendHelloMessage()
        self.peer_main_instance.udpClientSocket.sendto.assert_called()
        self.assertEqual(self.peer_main_instance.timer.is_alive(), True)


##Testiny peerClient Class


class TestPeerClient(unittest.TestCase):

    def setUp(self):
        # Create an instance of PeerClient with mock sockets
        self.peer_client_instance = PeerClient("127.0.0.1", 5000, "TestUser", MagicMock(), None)
        self.peer_client_instance.tcpClientSocket = MagicMock()

    def tearDown(self):
        # Cleanup any resources if needed
        pass

    def test_format_message_bold(self):
        # Test format_message for bold formatting
        input_message = '**Bold Text**'
        expected_output = '\033[1mBold Text\033[0m'
        result = self.peer_client_instance.format_message(input_message)
        self.assertEqual(result, expected_output)

    def test_format_message_italics(self):
        # Test format_message for italics formatting
        input_message = '*Italic Text*'
        expected_output = '\033[3mItalic Text\033[0m'
        result = self.peer_client_instance.format_message(input_message)
        self.assertEqual(result, expected_output)

    def test_format_message_hyperlinks(self):
        # Test format_message for hyperlinks formatting
        input_message = '[Link](https://www.example.com)'
        expected_output = '\033[4mLink\033[0m (https://www.example.com)'
        result = self.peer_client_instance.format_message(input_message)
        self.assertEqual(result, expected_output)

    def test_format_message_combined(self):
        # Test format_message for combined formatting
        input_message = '**Bold Text** and *Italic Text* with [Link](https://www.example.com)'
        expected_output = '\033[1mBold Text\033[0m and \033[3mItalic Text\033[0m with \033[4mLink\033[0m (https://www.example.com)'
        result = self.peer_client_instance.format_message(input_message)
        self.assertEqual(result, expected_output)


##Tesint peerserrver


class TestPeerServer(unittest.TestCase):

    def setUp(self):
        # Create an instance of PeerServer with mock sockets
        self.peer_server_instance = PeerServer("Abdelrahman", 5000)
        self.peer_server_instance.tcpServerSocket = MagicMock()

    def tearDown(self):
        # Cleanup any resources if needed
        pass

    def test_chat_request(self):
        # Test behavior when receiving a chat request
        self.peer_server_instance.run()
        self.peer_server_instance.tcpServerSocket.accept.assert_called()
        self.peer_server_instance.connectedPeerSocket.recv.return_value = "CHAT-REQUEST 1234 Abdelrahman"
        self.peer_server_instance.run()
        self.assertTrue(self.peer_server_instance.isChatRequested)
        self.assertEqual(self.peer_server_instance.connectedPeerPort, 1234)
        self.assertEqual(self.peer_server_instance.chattingClientName, "Abdelrahman")

    def test_chat_request_reject_busy(self):
        # Test rejecting chat request when already chatting
        self.peer_server_instance.isChatRequested = 1
        self.peer_server_instance.run()
        self.peer_server_instance.connectedPeerSocket.recv.return_value = "CHAT-REQUEST 1234 Abdelrahman"
        self.peer_server_instance.run()
        self.peer_server_instance.connectedPeerSocket.send.assert_called_with("BUSY".encode())

    def test_chat_request_reject(self):
        # Test rejecting chat request
        self.peer_server_instance.run()
        self.peer_server_instance.connectedPeerSocket.recv.return_value = "REJECT"
        self.peer_server_instance.run()
        self.assertEqual(self.peer_server_instance.isChatRequested, 0)

    def test_chat_request_accept(self):
        # Test accepting chat request
        self.peer_server_instance.run()
        self.peer_server_instance.connectedPeerSocket.recv.return_value = "OK"
        self.peer_server_instance.run()
        self.assertEqual(self.peer_server_instance.isChatRequested, 1)

    def test_receive_message(self):
        # Test receiving and displaying messages
        self.peer_server_instance.run()
        self.peer_server_instance.connectedPeerSocket.recv.return_value = "Hello, how are you?"
        self.peer_server_instance.run()
        self.assertEqual(
            self.peer_server_instance.connectedPeerSocket.send.call_args[0][0],
            "Abdelrahman: Hello, how are you?"
        )

    def test_quit_message(self):
        # Test handling quit message
        self.peer_server_instance.run()
        self.peer_server_instance.connectedPeerSocket.recv.return_value = ":q"
        self.peer_server_instance.run()
        self.assertEqual(self.peer_server_instance.isChatRequested, 0)


if __name__ == '__main__':
    unittest.main()
