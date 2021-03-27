import util
import socket
import client_responds

# Creates a HTTP/1.1 request
# command: the command of the HTTP/1.1 request
# host: the host that the request will be sent to
# path: path of the file you want to access
# port: port that will be used to access the server

def create_request(command: str, host: str, path: str, port: int) -> str:

    # Construct the http request message
    message = command + ' /' + path + ' HTTP/1.1\r\n'
    message += 'Host: ' + host + ':' + str(port) + '\r\n'
    message += 'Connection: keep-alive\r\n'
    # message += 'If-Modified-Since: Fri, Dec 31 23:59:59 2020 GMT' + '\r\n' # Uncomment this line to test
    message += '\r\n'

    # PUT or POST
    if command == 'PUT' or command == 'POST':
        user_input = input('Input: ')
        message += str(user_input)

    # print(message)
    return message

# sends a HTTP request given a socket and a request

def send(sock: socket, request: str) -> None:
    print("\r\nSending request...\r\n")
    message = request.encode(util.FORMAT)
    sock.send(message)


# Fetches all images from a html body
# will first find all paths to images in the body
# then creates HTTP/1.1 request to retrieve all the images

def fetch_images(body, host: str, port: int, sock: socket):
    paths = util.get_image_paths_from_html(body)
    for path in paths:
        img_request = create_request('GET', host, path, port)
        send(sock, img_request)
        client_responds.get_images_responds(sock, path)

