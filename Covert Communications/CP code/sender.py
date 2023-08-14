import socket
import os
import tqdm

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096

filename = 'meme.png'

fileSize = os.path.getsize(filename)

def send_data(data, host, port):
    """
    This function sends data from a buffer over TCP to the specified host and port.
    :param data: The data to be sent.
    :param host: The host to send the data to.
    :param port: The port to send the data to.
    """
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the host and port
    server_address = (host, int(port))
    sock.connect(server_address)


    progress = tqdm.tqdm(range(fileSize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transimission in 
            # busy networks
            sock.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))
    # close the socket
    sock.close()

    # try:
    #     # Send data
    #     # encode() converts string to bytes to send over the wire
    #     sock.send(f'{filename}{SEPARATOR}{fileSize}'.encode())
    #     print("Data sent: " + data)
    # finally:
    #     # Close the socket
    #     sock.close()

def main():
    # host variable is hardcoded to localhost (127.0.0.1), port is hardcoded to 8080
    # data is set to the single character "A"
    # Try changing these values or even allowing the user to input them at runtime or on the command line
    send_data(filename, "127.0.0.1", "8080")

main()
