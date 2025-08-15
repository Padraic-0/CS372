def get_tcp(file):
    with open(file, "rb") as fp:
        tcp_data = fp.read()
        tcp_length = len(tcp_data)  # <-- right here
        tcp_cksum = tcp_data[16:18]
        tcp_zero_cksum = tcp_data[:16] + b'\x00\x00' + tcp_data[18:]
        if len(tcp_zero_cksum) % 2 == 1:
            tcp_zero_cksum += b'\x00'
        return tcp_data, tcp_length, tcp_cksum, tcp_zero_cksum


def main():
    for l in range(9):
        tcp_data, tcp_length, tcp_cksum, tcp_zero_cksum = get_tcp(f"tcp_data_{l}.dat")
        with open(f"tcp_addrs_{l}.txt", "r") as fp:
            data = fp.read()
        data = data.rstrip()
        data = data.split(" ")
        data = ".".join(data)
        data = data.split(".")
        data.append(0)
        data.append(6)
        data.append(0) #length needs to be 16 bit, need to see how to pad
        data.append(tcp_length)
        pseudoheader = b''
        for x in range(len(data)):
            data[x] = int(data[x]).to_bytes(1,"big")
        pseudoheader = b''.join(data)
        data2 = pseudoheader + tcp_zero_cksum
        offset = 0   # byte offset into data
        total = 0    # check sum
        while offset < len(data2):
        # Slice 2 bytes out and get their value:
            word = int.from_bytes(data2[offset:offset + 2], "big")
            total += word
            total = (total & 0xffff) + (total >> 16)
            offset += 2   # Go to the next 2-byte value
        total = ((~total) & 0xffff)
        if total == int.from_bytes(tcp_cksum,"big"):
            print ("PASS")
        else:
            print("FAIL")
main()