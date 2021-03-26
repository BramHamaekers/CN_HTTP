import socket
import util
import shutil
import client_request
import os


def responds(sock: socket, command: str, host: str, port: int):
    if command == 'GET':
        get_responds(sock, host, port)
    if command == 'HEAD':
        head_responds(sock)


def get_responds(sock: socket, host: str, port: int) -> None:

    # Clear the output folder
    if os.path.isdir('output'):
        shutil.rmtree('output')

    # Parse head
    init: list[str] = sock.recv(1024).decode(util.FORMAT).split('\r\n')   # receive enough date so it includes HEADER

    separator = init.index('')  # Find index of separator between HEADER and BODY
    head = init[:separator]     # Split HEADER from BODY
    body = init[separator:]     # Split BODY from HEADER

    # Check which indication is used for the size of the body
    matching = [elem for elem in head if "Content-Length:" in elem]
    if 'Transfer-Encoding: chunked' in head:
        get_responds_chunked(sock, body, host, port)
    elif matching:  # if 'Content-Length is in header
        content_len: int = int(matching[0].split(' ')[1])   # Get Content-Length
        get_responds_cl(sock, content_len, body, host, port)


def get_responds_chunked(sock: socket, body: list, host: str, port: int) -> None:

    # Convert body back to string
    body = '\r\n'.join(body[2:])

    zero_line = False
    while True:
        recv = sock.recv(1024)
        recv = recv.decode(util.FORMAT)
        lines = recv.split('\r\n')

        for line in lines:
            if line == '0':
                zero_line = True
                body += '\r\n'.join(lines[:-3])
                break
        if zero_line:
            break

        body += recv

    # write body to html file
    util.write_html(body)

    # get all images
    client_request.fetch_images(body, host, port, sock)


# responds for GET command if encoding = Content-Length
def get_responds_cl(sock: socket, content_len: int, body: list, host: str, port: int) -> None:

    # Convert body back to string
    body = '\r\n'.join(body[1:])

    # Get length of body that was already received
    body_len: int = len(body.encode(util.FORMAT))
    curr_length = body_len

    # receive until content length is received
    while curr_length < content_len:
        recv = sock.recv(1024)
        recv = recv.decode(util.FORMAT)
        body += recv
        curr_length += len(recv)

    # write body to html file
    util.write_html(body)

    # get all images
    client_request.fetch_images(body, host, port, sock)


def get_images_responds(sock: socket, path):
    # Parse head
    init: list[str] = sock.recv(1024).decode(util.FORMAT).split('\r\n')  # receive enough data so it includes HEADER

    separator = init.index('')  # Find index of separator between HEADER and IMAGE
    head = init[:separator]  # Split HEADER from IMAGE
    img = init[separator:]  # Split IMAGE from HEADER

    # Find Content-Length of image
    matching = [elem for elem in head if "Content-Length:" in elem]
    content_len: int = int(matching[0].split(' ')[1])

    # Convert body back to encoded data
    img = '\r\n'.join(img[1:]).encode(util.FORMAT)

    # Get length of body that was already received
    img_len: int = len(img)
    curr_length = img_len

    # receive until content length is received
    while curr_length < content_len:
        recv = sock.recv(1024)
        img += recv
        curr_length += len(recv)

    # write image to image file
    util.write_image(img, path)


def head_responds(sock: socket) -> None:
    recv = sock.recv(1024)          # 1024 should be enough to receive HEAD
    recv = recv.decode(util.FORMAT)
    print(recv)
    return
