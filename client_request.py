import util
import socket
import client_responds


def create_request(command: str, host: str, path: str, port: int) -> str:

    # Construct the http request message
    message = command + ' /' + path + ' HTTP/1.1\r\n'
    message += 'Host: ' + host + ':' + str(port) + '\r\n'
    message += 'Connection: keep-alive\r\n'
    message += '\r\n'
    return message


def send(sock: socket, request: str) -> None:
    print("\r\nSending request...\r\n")
    message = request.encode(util.FORMAT)
    sock.send(message)


def fetch_images(body, host: str, port: int, sock: socket):
    paths = util.get_image_paths_from_html(body)
    for path in paths:
        img_request = create_request('GET', host, path, port)
        send(sock, img_request)
        client_responds.get_images_responds(sock, path)

