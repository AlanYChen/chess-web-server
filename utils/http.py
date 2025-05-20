TEST_GAME_PLACE_ID = "94859758442999"
OFFICIAL_GAME_PLACE_ID = "11354038241"

def sendHttpError(client_socket):
    response = 'HTTP/1.1 500 Internal Server Error\n\nfullErr'
    client_socket.sendall(response.encode())

def checkHttpRequest(request_lines):
    if request_lines[0] != "POST / HTTP/1.1":
        return False
    
    place_id_1 = f"Roblox-Id: {TEST_GAME_PLACE_ID}"
    place_id_2 = f"Roblox-Id: {OFFICIAL_GAME_PLACE_ID}"

    if place_id_1 not in request_lines and place_id_2 not in request_lines:
        return False
    return True