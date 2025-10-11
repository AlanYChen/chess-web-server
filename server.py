import socket, time, threading
from datetime import datetime
from utils.logger import log
from utils.http import checkHttpRequest, sendHttpError
from chessEngineRunner import get_total_engine_output
from chessEngine import shutdown_engines

PORT = 8000

def respond_to_client(client_socket):
    try:
        request = client_socket.recv(1024).decode()
    except UnicodeDecodeError as e:
        print(f"UnicodeDecodeError: {e}")
        sendHttpError(client_socket)
        return
    except ConnectionResetError as e:
        print(f"Connection reset by peer: {e}")
        return
    
    log(f"From client at {datetime.now().strftime("%m-%d %H:%M")}:")
    log(f"{request}")

    request_lines = request.splitlines()
    if checkHttpRequest(request_lines) == False:
        sendHttpError(client_socket)
        return

    total_engine_output = get_total_engine_output(request_lines)
    log(f"total_engine_output: {total_engine_output}")

    response = 'HTTP/1.1 200 OK\n\n' + total_engine_output
    client_socket.sendall(response.encode())
    client_socket.close()

def accept_connections_from_clients(server_socket):
     while True:
        try:
            client_socket, addr = server_socket.accept()
        except KeyboardInterrupt:
            print("Exiting")
            break

        start_time = time.time()

        client_handler = threading.Thread(target=respond_to_client, args=(client_socket, ))
        client_handler.start()

        end_time = time.time()
        log(f"Total server response time: {end_time - start_time}\n")

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Without this, even when socket is closed, the OS keeps the port in a TIME_WAIT state for a short duration, preventing the port from being reused immediately after
        server_socket.bind(("", PORT))
        server_socket.listen()
        print(f"Listening to port {PORT}")

        try:
            accept_connections_from_clients(server_socket)
        finally:
            shutdown_engines()

if __name__ == "__main__":
    run_server()