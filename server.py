import socket
import time
from chessEngine import run_engine, log

HOST = ""
PORT = 8000

def respond_to_client(client_socket):
    data = client_socket.recv(1024)
    request = data.decode()
    log(f"From client:\n{request}")

    lines = request.splitlines()
    
    # Ensure this is a POST request
    # http_method = lines[0].split(' ')[0]
    # if http_method != 'POST':
    #     response = 'HTTP/1.1 405 Method Not Allowed\n\nAllow: GET'
    #     client_socket.sendall(response.encode())
    #     return

    engine_outputs = []
    for fen in get_fens(lines):
        engine_outputs.append(run_engine(fen))
    
    total_engine_output = ','.join(engine_outputs)
    print(total_engine_output)

    response = 'HTTP/1.1 200 OK\n\n' + total_engine_output
    client_socket.sendall(response.encode())

def get_fens(lines):
    for i, line in enumerate(lines):
        if line == '':
            return lines[i + 1:]
    
    print(f"lines: {lines}")
    raise ValueError("get_fens received lines with no empty line")

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
            log(f"Total server response time: {end_time - start_time}\n")