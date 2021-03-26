import util
import mimetypes
from datetime import datetime
import pytz
import os


def get_or_head(request, connection, get: bool):
    print(request)

    # Parse HTTP header
    headers = request.split('\n')
    path = headers[0].split()[1]

    if path == '/':
        path = '/index.html'

    try:
        file = open('HTML PAGE' + path, 'rb')
        content = file.read()
        file.close()
    except FileNotFoundError:                       # 404 Not Found
        print("404 Not Found")
        file_not_found_responds_404(connection, get)
        return

    if 'Host: ' not in request:                     # 400 Bad Request
        bad_request_responds_400(connection, get)
        return

    content_len = len(content)

    # Send HTTP response
    response = b'HTTP/1.1 200 OK\r\n'               # 200 OK
    response += get_header(path, content_len)
    if get:
        response += b'\r\n' + content

    send(connection, response)


def put(request, connection):
    print(request)

    # Parse HTTP header
    headers = request.split('\r\n')
    path = headers[0].split()[1]



        #TODO: not allowed to change root path

    separator = headers.index('')  # Find index of separator between HEADER and BODY
    body = headers[separator + 1:]  # Split BODY from HEADER

    file = open('HTML PAGE' + path, 'a')    # open file in append mode
    for line in body:
        file.write(line)

    file.close()    # close the file
    return


def post(request, connection):
    print(request)

    # Parse HTTP header
    headers = request.split('\r\n')
    path = headers[0].split()[1]

    if path == '/':
        path = '/index.html'
        print("in here")
        return
        # TODO: not allowed to change root path

    separator = headers.index('')  # Find index of separator between HEADER and BODY
    body = headers[separator + 1:]  # Split BODY from HEADER

    # remove the file if it already exists and create the new resource
    file = open('HTML PAGE' + path, 'w+')  # open file in append mode
    for line in body:
        file.write(line)

    file.close()  # close the file
    return


def bad_request_responds_400(connection, get):

    # Get 400 Bad Request html page
    file = open('HTML PAGE/STATUS CODES/400.html', 'rb')
    content = file.read()
    file.close()

    response = b'HTTP/1.1 400 Bad Request\r\n'
    response += get_header('/STATUS CODES/400.html', len(content))
    if get:
        response += b'\r\n' + content

    send(connection, response)


def file_not_found_responds_404(connection, get):

    # Get 404 Not Found html page
    file = open('HTML PAGE/STATUS CODES/404.html', 'rb')
    content = file.read()
    file.close()

    response = b'HTTP/1.1 404 Not Found\r\n'
    response += get_header('/STATUS CODES/404.html', len(content))
    if get:
        response += b'\r\n' + content

    send(connection, response)


def get_header(path, content_len):

    # Get Date GMT
    date = datetime.now(pytz.utc)

    header = b'Content-Type: ' + bytes(str(mimetypes.guess_type('HTML PAGE' + path)[0]), util.FORMAT) + b'\r\n'
    header += b'Date: ' + bytes(date.strftime("%a, %d %b %Y %X GMT"), util.FORMAT) + b'\r\n'
    header += b'Content-Length: ' + bytes(str(content_len), util.FORMAT) + b'\r\n'

    return header


def send(connection, response):
    connection.sendall(response)

