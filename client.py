import socket
BYTES_TO_READ = 4096

def get(host, port):
    request = b"GET / HTTP/1.1\r\nHost: " + host.encode('utf-8') + b"\n\n"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET=>IPv4, SOCK_STREAM=>TCP.
    s.connect((host, port))
    s.send(request)
    s.shutdown(socket.SHUT_WR) # indicate finished, the write end is closed
    result = s.recv(BYTES_TO_READ) # keep reading incoming data
    while (len(result)>0):
        print(result)
        result = s.recv(BYTES_TO_READ)
    s.close()

#get("www.google.com", 80)
get("localhost", 8080) # or "127.0.0.1"