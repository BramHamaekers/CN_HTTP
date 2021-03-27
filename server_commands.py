import util
import mimetypes
from datetime import datetime
from dateutil.parser import parse
from tzlocal import get_localzone
import pytz
import os


# Handler for dealing with an incoming GET or HEAD command

def get_or_head(request, connection, get: bool):
    print(request)

    # UCOMMENT_THIS_LINE_FOR_500_SERVER_ERROR

    # Parse HTTP header
    headers = request.split('\r\n')
    path = headers[0].split()[1]

    if path == '/':
        path = '/index.html'

    if 'Host: ' not in request:                     # 400 Bad Request
        bad_request_responds_400(connection, get)
        return

    try:
        file = open('HTML PAGE' + path, 'rb')
        content = file.read()
        file.close()
    except FileNotFoundError:                       # 404 Not Found
        print("404 Not Found")
        file_not_found_responds_404(connection, get)
        return

    if 'If-Modified-Since: ' in request:
        check_modified_date(headers, path, connection)

    content_len = len(content)

    # Send HTTP response
    response = b'HTTP/1.1 200 OK\r\n'               # 200 OK
    response += get_header(path, content_len)
    if get:
        response += b'\r\n' + content

    send(connection, response)

# Handler for dealing with an incoming PUT command

def put(request, connection):
    print(request)

    # Parse HTTP header
    headers = request.split('\r\n')
    path = headers[0].split()[1]

    if path == '/':     # Not allowed to change root path
        return

    separator = headers.index('')  # Find index of separator between HEADER and BODY
    body = headers[separator + 1:]  # Split BODY from HEADER

    file = open('HTML PAGE' + path, 'a')    # open file in append mode
    for line in body:
        file.write(line)

    file.close()    # close the file
    return


# Handler for dealing with an incoming POST command

def post(request, connection):
    print(request)

    # Parse HTTP header
    headers = request.split('\r\n')
    path = headers[0].split()[1]

    if path == '/':     # Not allowed to change root path
        return

    separator = headers.index('')  # Find index of separator between HEADER and BODY
    body = headers[separator + 1:]  # Split BODY from HEADER

    # remove the file if it already exists and create the new resource
    file = open('HTML PAGE' + path, 'w+')  # open file in append mode
    for line in body:
        file.write(line)

    file.close()  # close the file
    return


# Function for dealing with 'If-Modified-Since header
# will do nothing if the file was modified since the given date
# this will result in normal GET behavior
# If the file was modified since the given date
# HTTP/1.1 304 Not Modified Responds will be sent to the client

def check_modified_date(headers, path, connection):

    # Get Date from header
    matching = [elem for elem in headers if "If-Modified-Since:" in elem]
    header_date = parse(' '.join(matching[0].split(' ')[1:]))

    # Get modification date
    local_tz = str(get_localzone())                             # Get local timezone
    mod_time_since = os.path.getmtime('HTML PAGE' + path)       # Get date of modification
    modification_date = datetime.fromtimestamp(mod_time_since)  # Convert to readable timestamp

    # Convert to GMT
    local = pytz.timezone(local_tz)
    local_dt = local.localize(modification_date, is_dst=None)
    gmt_modification_date = local_dt.astimezone(pytz.utc)       # GMT time of modification date.

    if header_date < gmt_modification_date:                     # If the file has been modified since:
        return                                                  # Do nothing -> Will result in normal GET behavior

    # Get Date GMT
    date = datetime.now(pytz.utc)

    # Send 304 Not Modified
    response = b'HTTP/1.1 304 Not Modified\r\n'
    response += b'Date: ' + bytes(date.strftime("%a, %d %b %Y %X GMT"), util.FORMAT) + b'\r\n'
    send(connection, response)


# Will send a 'HTTP/1.1 400 Bad Request' response to the client
# along with the '400.html' body

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


# Will send a 'HTTP/1.1 404 Not Found' response to the client
# along with the '404.html' body

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

# Retrieves a header including 'Content-Type', 'Date' and 'Content-Length
# given a path and the content_len of a file

def get_header(path, content_len):

    # Get Date GMT
    date = datetime.now(pytz.utc)

    header = b'Content-Type: ' + bytes(str(mimetypes.guess_type('HTML PAGE' + path)[0]), util.FORMAT) + b'\r\n'
    header += b'Date: ' + bytes(date.strftime("%a, %d %b %Y %X GMT"), util.FORMAT) + b'\r\n'
    header += b'Content-Length: ' + bytes(str(content_len), util.FORMAT) + b'\r\n'

    return header


# Sends a HTTP response to a client given a connection and a response

def send(connection, response):
    connection.sendall(response)

