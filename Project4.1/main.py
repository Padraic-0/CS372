import datetime
import socket

def system_seconds_since_1900():
    """
    The time server returns the number of seconds since 1900, but Unix
    systems return the number of seconds since 1970. This function
    computes the number of seconds since 1900 on the system.
    """

    # Number of seconds between 1900-01-01 and 1970-01-01
    seconds_delta = 2208988800

    seconds_since_unix_epoch = int(datetime.datetime.now().strftime("%s"))
    seconds_since_1900_epoch = seconds_since_unix_epoch + seconds_delta

    return seconds_since_1900_epoch
s = socket.socket()
server = 'time.nist.gov'
port = 37
connect_arg = server, port

s.connect(connect_arg)

response = b''
while True:
    buffer = s.recv(4096)
    if buffer == b'':
        break
    response += buffer
s.close()

time = int.from_bytes(response,"big")

print(f"System Time: {system_seconds_since_1900()}")
print(f"Gov Time: {time}")
print(f"Gov Time as Date: {datetime.datetime.fromtimestamp(time - 2208988800 )}")






