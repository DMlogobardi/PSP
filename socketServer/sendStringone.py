
import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 12345  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.send("afjaksfh!i!1!sUd1X!39dfa55283318d31afe5a3ff4a0e3253e2045e43!2023/04/02 16:27:07!UjQx3".encode())
    data = s.recv(1024)

print(f"Received {data!r}")