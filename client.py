import client_input
import client_request
import client_responds
import socket

import util
# Global variables


CONNECTED: bool = False
SOCKET: socket
HOST: str
PORT: int


def connect(uri: str, port: int) -> None:
    global CONNECTED
    global SOCKET
    global HOST
    global PORT

    # connect the socket
    host: str = util.get_host_from_uri(uri)
    server_address: tuple = (host, port)
    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SOCKET.connect(server_address)
    CONNECTED = True
    HOST = host
    PORT = port


# https://stackoverflow.com/questions/47658584/implementing-http-client-with-sockets-without-http-libraries-with-python
def main() -> None:

    try:
        # Get http request input.
        input: list[str] = client_input.get_input()
    except SystemExit:
        # close program on SystemExit error
        exit()
    except:
        # If input was not valid, try again
        main()
    else:
        # Assign input values
        command: str = input[util.COMMAND_INDEX]
        uri: str = input[util.URI_INDEX]
        port: int = int(input[util.PORT_INDEX])
        # If input was valid, handle the request
        connect(uri, port)  # connect with uri and port

        # extract host and path from uri
        host: str = util.get_host_from_uri(uri)
        path: str = util.get_path_from_uri(uri)

        request: str = client_request.create_request(command, host, path, port)
        client_request.send(SOCKET, request)
        client_responds.responds(SOCKET, command, host, port)

        print('Request completed')

def get_socket() -> socket:
    print(CONNECTED)
    return SOCKET


# Call the main method
if __name__ == "__main__":
    main()


