# Note: same behavior as client.py, modified with chunk support

import socket
BYTES_TO_READ = 4096

def get(host, port):
    request = b"GET / HTTP/1.1\r\nHost: " + host.encode('utf-8') + b"\n\n"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # AF_INET=>IPv4, SOCK_STREAM=>TCP.
        s.connect((host, port))
        s.send(request)
        s.shutdown(socket.SHUT_WR) # indicate finished, the write end is closed

        # Allow for chunk data
        chunk = s.recv(BYTES_TO_READ) # start reading incoming data
        result = b'' + chunk

        while (len(chunk)>0):
            chunk = s.recv(BYTES_TO_READ) # keep reading incoming data
            result += chunk

        s.close()
        return result

#get("www.google.com", 80)
print(get("localhost", 8080)) # or "127.0.0.1"
