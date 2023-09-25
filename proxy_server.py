import socket
from threading import Thread
BYTES_TO_READ = 4096
HOST = "127.0.0.1" # equivalent to HOST = "localhost"
PORT = 8080

def send_request(host, port, request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # AF_INET=>IPv4, SOCK_STREAM=>TCP.
        s.connect((host, port))
        s.send(request)
        s.shutdown(socket.SHUT_WR) # indicate finished, the write end is closed

        # Allow for chunk data
        data = s.recv(BYTES_TO_READ) # start reading incoming data
        result = b'' + data
        while len(data) > 0:
            data = s.recv(BYTES_TO_READ) # keep reading incoming data
            result += data

        return result

def handle_connection(conn, addr): # conn=>new socket object, addr=>(Client's IP address, TCP port number)
    with conn:
        print(f"Connected by {addr}")
        request = b''

        while True:
            data = conn.recv(BYTES_TO_READ)
            # if no more client "talk", full request has been sent
            if not data: # i.e. break when receive b''
                break
            print(f"Data received {data}") # Step 2.
            request += data

        # pass on the request then return the repsonse to the client
        response = send_request("www.google.com", 80, request)
        conn.sendall(response)

def start_server():
    # act first as server, but handle connection now by also acting as a client (forward request)
    # initialize socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # bind, listen, and accept connection
        s.bind((HOST, PORT))

        # SOL_SOCKET=>socket layer. SO_REUSEADDR=>set the reusability of the socket during linger.
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.listen(2)
        conn, addr = s.accept() # conn=>socket at client side  # addr=>(IP, Port of client)
        handle_connection(conn, addr)

def start_threaded_server():
    # act first as server, but handle connection now by also acting as a client (forward request)
    # initialize socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # bind, listen, and accept connection
        s.bind((HOST, PORT))

        # SOL_SOCKET=>socket layer. SO_REUSEADDR=>set the reusability of the socket during linger.
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.listen(2)

        # for threading
        while True:
            conn, addr = s.accept()
            thread = Thread(target=handle_connection, args=(conn, addr))
            thread.run()

#start_server()
start_threaded_server()
