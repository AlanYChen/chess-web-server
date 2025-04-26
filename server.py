import socket, time
from datetime import datetime
from logger import log
from chessEngineRunner import get_total_engine_output
from chessEngine import re_instantiate_engines, shutdown_engines

PORT = 8000

def respond_to_client(client_socket):
    try:
        request = client_socket.recv(1024).decode()
    except UnicodeDecodeError as e:
        print(f"UnicodeDecodeError: {e}")

        response = 'HTTP/1.1 200 OK\n\n' + "fullErr"
        client_socket.sendall(response.encode())
        return False
    
    log(f"From client at {datetime.now().strftime("%m-%d %H:%M")}:")
    log(f"{request}")

    total_engine_output = get_total_engine_output(request)
    log(f"total_engine_output: {total_engine_output}")

    response = 'HTTP/1.1 200 OK\n\n' + total_engine_output
    client_socket.sendall(response.encode())

    engine_error = (total_engine_output[-3:] == "err")
    return engine_error

def accept_connections_from_clients(server_socket):
     while True:
        try:
            client_socket, addr = server_socket.accept()
        except KeyboardInterrupt:
            print("Exiting")
            break

        with client_socket:
            start_time = time.time()
            engine_error = respond_to_client(client_socket)
            end_time = time.time()
            log(f"Total server response time: {end_time - start_time}\n")

        if engine_error:
            log(f"engine_error: {engine_error}")
            re_instantiate_engines()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(("", PORT))
    server_socket.listen()
    print(f"Listening to port {PORT}")

    try:
        accept_connections_from_clients(server_socket)
    finally:
        shutdown_engines()