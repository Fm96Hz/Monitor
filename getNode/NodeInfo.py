import socket
import json

def message():
    tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_client_socket.connect(("127.0.0.1", 9000))
    send_data = "Request NodeInfo".encode("utf-8")
    tcp_client_socket.send(send_data)
    recv_data = tcp_client_socket.recv(1024)
    tcp_client_socket.close()

    recv_content = recv_data.decode("utf-8")
    return json.loads(recv_content)






