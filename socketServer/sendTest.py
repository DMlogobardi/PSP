
import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 12345  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    oldStr=    "966e!i!2!WbE9w!28de886668864c3e6d890e623ae7ea944253e502!2023/05/17 18:44:55!xJQ6p"
    s.send("afjaksfh!i!1!sUd1X!39dfa55283318d31afe5a3ff4a0e3253e2045e43!2023/04/02 22:37:07!UjQx3".encode())
    data = s.recv(1024)

print(f"Received {data!r}")