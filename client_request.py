import util
import socket


def create_request(command: str, uri: str, port: int) -> str:

    # extract host and path from uri
    host: str = util.get_host_from_uri(uri)
    path: str = util.get_path_from_uri(uri)

    # Construct the http request message
    message = command + ' /' + path + ' HTTP/1.1\r\n'
    message += 'Host: ' + host + ':' + str(port) + '\r\n'
    message += 'Connection: keep-alive\r\n'
    message += '\r\n'
    return message


def send(SOCKET: socket, request):
    print("\r\nSending request...\r\n")
    message = request.encode(util.FORMAT)
    SOCKET.send(message)

