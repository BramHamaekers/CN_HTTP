import socket
import util

# define custom exceptions
from util import get_host_from_uri, COMMAND_INDEX, URI_INDEX, PORT_INDEX


class InvalidCommand(Exception):
    pass
class InvalidURI(Exception):
    pass
class InvalidPort(Exception):
    pass


# Ask the user for input and check if the given input by the user is a valid input.
def get_input():

    # Get input
    val = input('>: ')
    val = val.split(' ')

    # User can close program by typing command 'CLOSE'
    if len(val) == 1 and val[0] == 'CLOSE':
        raise SystemExit
    try:
        is_valid_command(val[util.COMMAND_INDEX])
        is_valid_port(val[util.PORT_INDEX])  # check port before uri for improved performance.
        is_valid_uri(val[util.URI_INDEX])
    except InvalidCommand as err:
        print('InvalidCommand: Command ' + val[util.COMMAND_INDEX] + ' is not a valid command')
        raise err
    except InvalidURI as err:
        print('InvalidURI: URI ' + val[util.URI_INDEX] + ' is not a valid URI')
        raise err
    except InvalidPort as err:
        print('InvalidPort: Port ' + val[util.PORT_INDEX] + ' is not a valid port')
        raise err
    return val


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
        val = int(port)
        if val < 0:  # if not a positive int raise InvalidPort
            raise InvalidPort
    except ValueError:  # if port is not an int raise InvalidPort
        raise InvalidPort

