# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select

def run_server(port):
    # TODO--fill this in
    pass
    address = ''
    bind_v = address, port
    s = socket.socket()
    s.bind(bind_v)
    s.listen()
    ready_set = {s}
    while True:
        ready_to_read, _, _ = select.select(ready_set, {}, {})
        for j in ready_to_read:
            if j == s:
                j = s.accept()
                print(f"{j[0].getpeername()} Connected")
                ready_set.add(j[0])
            else:
                print(j.getpeername(), end=" ")
                info = b""
                data = j.recv(4096)
                if len(data) != 0:
                    print(f"{len(data)} Bytes", end=" ")
                    info += data
                    print(data)
                else:
                    print(f"{j.getpeername()} Disconnected")
                    ready_set.remove(j)
                
    

#--------------------------------#
# Do not modify below this line! #
#--------------------------------#

def usage():
    print("usage: select_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
