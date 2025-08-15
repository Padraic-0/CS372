import socket
import sys
import os


def request_handle (request):
    request = request.decode("ISO-8859-1")
    header = request.split("\r\n")

    get = header[0].split()
    file_path = get[1].split("/")
    file_path = file_path[-1]
    print(file_path)
    return file_handle(file_path)

def file_handle(file_path):
    try:
        with open(file_path, "r") as fp:
            data = fp.read()
            Content_Length = len(data)
            #data = data.encode("ISO-8859-1")
            Content_Type = get_mime(file_path)
            response = "HTTP/1.1 200 OK"
    except:
        data = "404 Not Found"
        Content_Length = len(data)
        Content_Type = "text/plain"
        response = "HTTP/1.1 200 OK"
    header = f"{response}\r\nContent-Type: {Content_Type}\r\nContent-Length:{Content_Length}\r\nConnection: close\r\n\r\n{data}"
    print(header)
    #"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 6\r\nConnection: close\r\n\r\nHello!".encode("ISO-8859-1")
    return header

def get_mime(file_path):
    a = os.path.splitext(file_path)
    file_type = a[1]
    if file_type == ".txt":
        return "text/plain"
    if file_type == ".html":
        return "text/html"
    else:
        return "text/plain"
try:
  port = sys.argv[1]
except:
    port = 28333
address = ''
bind_v = address,int(port)

s = socket.socket()
s.bind(bind_v)
s.listen()

blank_line = '\r\n\r\n'.encode("ISO-8859-1")

while True:
    new_conn = s.accept()
    new_socket = new_conn[0]
    request = b""

    while True:
        d = new_socket.recv(4096)
        request += d
        #print(request)
        if request.find(blank_line) != False:
            break

    header = request_handle(request).encode("ISO-8859-1")
    new_socket.sendall(header)
    new_socket.close()
    


    


