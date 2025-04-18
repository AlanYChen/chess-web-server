import socket, time
from logger import log
from chessEngineRunner import get_total_engine_output
from chessEngine import re_instantiate_engine

PORT = 8000

def respond_to_client(client_socket):
    request = client_socket.recv(1024).decode()
    # log(f"From client:\n{request}")

    total_engine_output = get_total_engine_output(request)
    log(f"total_engine_output: {total_engine_output}")

    response = 'HTTP/1.1 200 OK\n\n' + total_engine_output
    client_socket.sendall(response.encode())

    error_occurred = (total_engine_output[-3:] == "err")
    return error_occurred

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(("", PORT))
    server_socket.listen()
    print(f"Listening to port {PORT}")

    while True:
        try:
            client_socket, addr = server_socket.accept()
        except KeyboardInterrupt:
            print("Exiting")
            break

        with client_socket:
            start_time = time.time()
            error_occurred = respond_to_client(client_socket)
            end_time = time.time()
            log(f"Total server response time: {end_time - start_time}\n")

        log(f"error_occurred:", error_occurred)
        if error_occurred:
            re_instantiate_engine()