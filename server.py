import socket
import threading
import util
import server_commands


HEADER = 1024
DISCONNECT_MESSAGE = "DISCONNECT!"


def start_server(server):
    server.listen()

    # Create first thread for client
    t = threading.Thread(target=handle_client, args=(server,))
    t.start()


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

            if 'GET' in request:
                server_commands.get(request, conn)
            elif request == "":                 # close connection if client sends an empty request
                connected = False
            else:
                print(request)

            # exception occurs when terminal client closes connection -> close connection with socket
        except ConnectionResetError:
            connected = False
    print("[CLOSE CONNECTION]", addr[0], "disconnected.")
    conn.close()


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