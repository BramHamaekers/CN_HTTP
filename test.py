import socket

FORMAT = 'latin_1'


# message formate
# command 'path' HTTP/1.1
server_address = ('www.tcpipguide.com', 80)
message = 'GET /pricing.htm HTTP/1.1\r\n'
message += 'Host: www.tcpipguide.com:80\r\n'
message += 'Connection: keep-alive\r\n'
message += '\r\n'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(server_address)
sock.send(message.encode(FORMAT))

data = ''
while True:
    buf = sock.recv(1024).decode(FORMAT)
    if not buf:
        break
    data += buf

print(data)


