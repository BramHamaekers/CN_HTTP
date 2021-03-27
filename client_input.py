import socket
import util
from util import get_host_from_uri


# define custom exceptions

class InvalidCommand(Exception):
    pass


class InvalidURI(Exception):
    pass


class InvalidPort(Exception):
    pass


# Checks if the given arguments are valid arguments for the HTTP client
# arguments: The arguments given when running the program

def check_input(arguments):

    # Get input
    args: list = arguments[1:]

    # User can close program by typing command 'CLOSE'
    if len(args) == 1 and args[0] == 'CLOSE':
        raise SystemExit
    elif not len(args) == 3:
        print('Request should have 3 arguments:[COMMAND] [URI] [PORT]')
    try:
        is_valid_command(args[util.COMMAND_INDEX])
        is_valid_port(args[util.PORT_INDEX])  # check port before uri for improved performance.
        is_valid_uri(args[util.URI_INDEX])
    except InvalidCommand as err:
        print('InvalidCommand: Command ' + args[util.COMMAND_INDEX] + ' is not a valid command')
        raise err
    except InvalidURI as err:
        print('InvalidURI: URI ' + args[util.URI_INDEX] + ' is not a valid URI')
        raise err
    except InvalidPort as err:
        print('InvalidPort: Port ' + args[util.PORT_INDEX] + ' is not a valid port')
        raise err
    return args


# Check if the first argument of input is a valid command.
# if command is not a valid command: raise InvalidCommand

def is_valid_command(command: str) -> None:
    if command == 'HEAD' or command == 'GET' or command == 'PUT' or command == 'POST':
        return
    else:
        raise InvalidCommand


# Check if the second argument of input is a valid uri.
# if uri is not a valid uri: raise InvalidURI

def is_valid_uri(uri: str) -> None:
    try:
        host = get_host_from_uri(uri)
        socket.gethostbyname(host)
    except:
        raise InvalidURI


# Check if the third argument of input is a valid uri.
# if uri is not a valid uri: raise InvalidPort

def is_valid_port(port: str) -> None:
    try:
        val: int = int(port)
        if val < 0:  # if not a positive int raise InvalidPort
            raise InvalidPort
    except ValueError:  # if port is not an int raise InvalidPort
        raise InvalidPort

