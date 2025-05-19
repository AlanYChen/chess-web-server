
def sendHttpError(client_socket):
    response = 'HTTP/1.1 500 Internal Server Error\n\nfullErr'
    client_socket.sendall(response.encode())

def checkHttpRequest(request_lines):
    print(request_lines)
    if request_lines[0] != "POST / HTTP/1.1":
        return False
    if "Roblox-Id: 94859758442999" not in request_lines:
        return False
    return True