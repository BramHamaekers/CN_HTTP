import sys
import client_input
import client_request
import client_responds
import socket

import util
# Global variables


SOCKET: socket


# Establishes a Connection to a server
# uri: uri of the server you want to connect to
# port: port you want to use to connect to a server

def connect(uri: str, port: int) -> None:
    global SOCKET

    # connect the socket
    host: str = util.get_host_from_uri(uri)
    server_address: tuple = (host, port)
    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SOCKET.connect(server_address)


# Main method of the HTTP client
# First check is the given input arguments are correct arguments
# then handles this input arguments following the standard http protocol

def main() -> None:

    try:
        # Check http request input.
        args: list[str] = client_input.check_input(sys.argv)
    except Exception as err:
        # If input was not valid, try again
        exit()
    else:
        # Assign input values
        command: str = args[util.COMMAND_INDEX]
        uri: str = args[util.URI_INDEX]
        port: int = int(args[util.PORT_INDEX])
        # If input was valid, handle the request
        connect(uri, port)  # connect with uri and port

        # extract host and path from uri
        host: str = util.get_host_from_uri(uri)
        path: str = util.get_path_from_uri(uri)

        # create request and send it to the server
        request: str = client_request.create_request(command, host, path, port)
        client_request.send(SOCKET, request)
        client_responds.responds(SOCKET, command, host, port)

        print('Request completed')


# Call the main method
if __name__ == "__main__":
    main()


