# Simple Python HTTP server to serve HTML UI
import socket
import sys
import os

HOST = ''
PORT = 8888

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket Created!!")
# Bind socket to local host and port
try:
    serversocket.bind((HOST, PORT))
except socket.error as msg:
    print("Bind failed. Error Code: " + str(msg[0]) + " Message: " + str(msg[1]))
    sys.exit()
print("Socket bind complete")

# Start Listening to Socket

serversocket.listen(5)
print(f'Socket now listening on port {PORT}')
# Establish the connection
while True:
    connectionSocket, addr = serversocket.accept()
    print('source address:', addr)
    try:
        # Recieve message from the socket
        message = connectionSocket.recv(1024).decode()
        print('message =', message)
        if not message:
            connectionSocket.close()
            continue
        #obtain file name from HTTP request
        request_line = message.splitlines()[0]
        parts = request_line.split()
        if len(parts) < 2 or parts[0] != 'GET':
            connectionSocket.send(b'HTTP/1.1 400 Bad Request\r\n\r\n')
            #Close the client socket
            connectionSocket.close()
            continue
        filename = parts[1]
        if filename == '/':
            filename = '/index.html'
        filepath = filename[1:]  # remove leading '/'
        if not os.path.isfile(filepath):
            #send response meaasge for file not found
            connectionSocket.send(b'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n')
            connectionSocket.send(b'<h1>404 Not Found</h1>')
            #Close the clinet socket
            connectionSocket.close()
            print("File not found, connection closed!")
            continue
        with open(filepath, 'rb') as f:
            outputdata = f.read()
        #send http header line to socket
        header = b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: ' + str(len(outputdata)).encode() + b'\r\nConnection: close\r\n\r\n'
        connectionSocket.send(header)
        #send content of requested file to client
        connectionSocket.sendall(outputdata)
        print("Served:", filepath)
        #close the connection socket
        connectionSocket.close()
        print("Connection closed!")
    except Exception as e:
        print("Error:", e)
        try:
            connectionSocket.send(b'HTTP/1.1 500 Internal Server Error\r\n\r\n')
            connectionSocket.close()
        except:
            pass
