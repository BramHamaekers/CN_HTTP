import socket
import util


def responds(sock: socket, command: str):
    if command == 'GET':
        get_responds(sock)
    if command == 'HEAD':
        head_responds(sock)


def get_responds(sock: socket):

    # Parse head
    init: list[str] = sock.recv(1024).decode(util.FORMAT).split('\r\n')   # receive enough date so it includes HEADER

    separator = init.index('')  # Find index of separator between HEADER and BODY
    head = init[:separator]     # Split HEADER from BODY
    body = init[separator:]     # Split BODY from HEADER

    # Check which indication is used for the size of the body
    matching = [elem for elem in head if "Content-Length:" in elem]
    if 'Transfer-Encoding: chunked' in head:
        get_responds_chunked(sock, body)
    elif matching:  # if 'Content-Length is in header
        content_len: int = int(matching[0].split(' ')[1])   # Get Content-Length
        get_responds_cl(sock, content_len, body)


def get_responds_chunked(sock, body):

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
    util.get_image_paths_from_html(body)


# responds for GET command if encoding = Content-Length
def get_responds_cl(sock: socket, content_len, body):

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
    util.get_image_paths_from_html(body)


def head_responds(sock: socket):
    recv = sock.recv(1024)          # Not a clean way of doing it, 1024 should be enough to receive HEAD
    recv = recv.decode(util.FORMAT)
    print(recv)
    return
