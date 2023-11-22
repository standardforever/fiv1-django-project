import socket
import threading

# Define the server's address and port
HOST = '127.0.0.1'
PORT = 8000

# Function to handle incoming WebSocket connections
def handle_client(client_socket):
    # This function will be called for each incoming connection
    request = client_socket.recv(1024).decode()

    # Extract the WebSocket key from the request
    key = ''
    for line in request.split('\n'):
        if 'Sec-WebSocket-Key' in line:
            key = line.split(': ')[1].strip()
            break

    # Construct the WebSocket response
    response = (
        'HTTP/1.1 101 Switching Protocols\r\n'
        'Upgrade: websocket\r\n'
        'Connection: Upgrade\r\n'
        f'Sec-WebSocket-Accept: {key}\r\n\r\n'
    )

    # Send the response to the client
    client_socket.send(response.encode())

    while True:
        # Receive and decode WebSocket data
        data = client_socket.recv(1024)
        if not data:
            break

        # Implement WebSocket data processing here
        # This example just prints the received data
        print(data.decode())

    # Close the client socket
    client_socket.close()

# Create the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print(f"[*] Listening on {HOST}:{PORT}")

while True:
    # Accept incoming connections and spawn a new thread for each
    client, addr = server.accept()
    print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
    
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
