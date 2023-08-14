import socket
import tqdm
import os

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
ipAddr = '127.0.0.1'
port = 8080

def receive_data(host, port, buffer_size):
    """
    This function receives data from TCP and writes it into a buffer.
    :param host: The host to receive data from.
    :param port: The port to receive data from.
    :param buffer_size: The size of the buffer to receive data into.
    :return: The received data.
    """
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the host and port
    server_address = (host, int(port))
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(5)

    # Wait for a connection
    connection, client_address = sock.accept()

    data = connection.recv(buffer_size).decode()
    filename, filesize = data.split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)


    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        while True:
            # read 1024 bytes from the socket (receive)
            bytes_read = connection.recv(BUFFER_SIZE)
            if not bytes_read:    
                # nothing is received
                # file transmitting is done
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))

    # close the client socket
    connection.close()
    # close the server socket
    sock.close()

    # try:
    #     # Receive data
    #     data = connection.recv(buffer_size).decode()
    #     filename, filesize = data.split(SEPARATOR)
    #     return data
    # finally:
    #     # Clean up the connection
    #     connection.close()

def main():
    # host variable is hardcoded to localhost (127.0.0.1), port is hardcoded to 8080, and buffer_size of 50
    # Try changing these values or even allowing the user to input them at runtime or on the command line
    print("Data received: " + receive_data(ipAddr, port, BUFFER_SIZE))

main()