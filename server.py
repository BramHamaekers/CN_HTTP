import socket
import threading
import util
import server_commands


HEADER = 1024
DISCONNECT_MESSAGE = "DISCONNECT!"


# Start listening for requests by a client
# Create a thread for a first client

def start_server(server):
    server.listen()

    # Create first thread for client
    t = threading.Thread(target=handle_client, args=(server,))
    t.start()


# accepts incoming connections
# when a connection is accepted a new thread is created
# to allow multiple clients to connect to the server at the same time

def handle_client(server):
    conn, addr = server.accept()  # accept method is a blocking method.
    print("[NEW CONNECTION]", addr[0], "connected")
    connected = True

    # create new thread for new client.
    t = threading.Thread(target=handle_client, args=(server,))
    t.start()

    while connected:
        try:
            request = conn.recv(HEADER).decode(util.FORMAT)
            print(request)

            # Check which command was included in the HTTP request

            if 'GET' in request:
                server_commands.get_or_head(request, conn, True)
            elif 'HEAD' in request:
                server_commands.get_or_head(request, conn, False)
            elif 'PUT' in request:
                server_commands.put(request, conn)
            elif 'POST' in request:
                server_commands.post(request, conn)
            elif request == "":                 # close connection if client sends an empty request
                connected = False
            else:
                print(request)

            # exception occurs when terminal client closes connection -> close connection with socket
        except ConnectionResetError:
            connected = False
        except Exception as err:        # Catch all other errors and send 500 Server Error
            print('[ERROR]:', err)
            response = b'HTTP/1.1 500 Server Error\r\n'
            server_commands.send(conn, response)

    print("[CLOSE CONNECTION]", addr[0], "disconnected.")
    conn.close()


# Main method of the HTTP server
# First opens the server connection
# Then starts the server functionality for dealing with HTTP requests

def main() -> None:

    # assign port and get ip address

    port = 5055
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)

    # create the server

    server_address: tuple = (ip, port)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(server_address)
    start_server(server)
    print("[SERVER CREATED]:", ip, port)


# Call the main method
if __name__ == "__main__":
    main()
