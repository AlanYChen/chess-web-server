import socket
# import time
from chessEngine import run_engine

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

print("Listening on port {}".format(PORT))

def respond_to_client(client_socket):
    data = client_socket.recv(1024)
    request = data.decode()
    # print(f"From client: {request}")

    lines = request.split('\n')
    http_method = lines[0].split(' ')[0]

    if http_method != 'POST':
        response = 'HTTP/1.1 405 Method Not Allowed\n\nAllow: GET'
        client_socket.sendall(response.encode())
        return
    
    # print(f"lines: {lines}")

    fen = lines[4]
    best_move = run_engine(fen)

    response = 'HTTP/1.1 200 OK\n\n' + best_move
    client_socket.sendall(response.encode())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    while True:
        try:
            client_socket, addr = s.accept()
        except KeyboardInterrupt:
            print("Exiting")
            break

        with client_socket:
            # start_time = time.time()
            respond_to_client(client_socket)
            # end_time = time.time()
            # print(f"Total server response time:{end_time - start_time}")