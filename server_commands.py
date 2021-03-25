import util
import mimetypes

def get(request, connection):
    print("[REQUEST]: GET")
    print(request)

    # Parse HTTP header
    headers = request.split('\n')
    path = headers[0].split()[1]

    # Get content of the file
    if path == '/':
        path = '/index.html'

    file = open('HTML PAGE' + path, encoding=util.FORMAT)
    content = file.read()
    file.close()

    # Send HTTP response
    response = 'HTTP/1.1 200 OK\r\n'
    response += 'Content-Type: ' + str(mimetypes.guess_type('HTML PAGE' + path)[0]) + '\r\n'
    response += 'Content-Length: ' + str(len(content)) + '\r\n'
    response += '\r\n' + content
    connection.sendall(response.encode(util.FORMAT))
