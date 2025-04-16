import socket
import time
from chessEngine import run_engine, log

HOST = ""
PORT = 8000  # Port to listen on (non-privileged ports are > 1023)

def respond_to_client(client_socket):
    data = client_socket.recv(1024)
    request = data.decode()
    log(f"From client: {request}")

    lines = request.split('\n')
    http_method = lines[0].split(' ')[0]

    if http_method != 'POST':
        response = 'HTTP/1.1 405 Method Not Allowed\n\nAllow: GET'
        client_socket.sendall(response.encode())
        return

    fen = lines[-1]
    best_move = run_engine(fen)

    response = 'HTTP/1.1 200 OK\n\n' + best_move
    client_socket.sendall(response.encode())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Listening to port {} ...".format(PORT))

    while True:
        try:
            client_socket, addr = s.accept()
        except KeyboardInterrupt:
            print("Exiting")
            break

        with client_socket:
            start_time = time.time()
            respond_to_client(client_socket)
            end_time = time.time()
            log(f"Total server response time:{end_time - start_time}\n")