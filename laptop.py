import socket
import os
import laptop
import webcam as wb
import time

HOME_LAPTOP = ""
HOME_PI = ""

CURRENT_LAPTOP = HOME_LAPTOP
LAPTOP_PORT = 1420
CURRENT_PI = HOME_PI
PI_PORT = 1421

## Recieves initial data from Pi in order to create the execution loop
def receive_data():
    #  Create a socket object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = CURRENT_LAPTOP
    port = LAPTOP_PORT

    #  Bind the socket to a specific IP and Port and listen for incoming connections
    server.bind((server_ip, port))
    server.listen()
    print(f"\n\tLaptop: Server Initialized. Listening on {server_ip}:{port}")

    #  Accept incoming connections
    client_socket, client_address = server.accept()
    print(f"\tLaptop: Accepted connection from {client_address[0]}:{client_address[1]}\n")
    print("Receiving data now...")

    #  Receive max_posts from the Pi
    while True:
        max_posts = client_socket.recv(2048).decode("utf-8")  #  Convert bytes to string

        client_socket.send("received".encode("utf-8"))
        break

    #  Receive interval_between_scans from the Pi
    while True:
        interval_between_scans = client_socket.recv(2048).decode("utf-8")  #  Convert bytes to string

        client_socket.send("received".encode("utf-8"))
        break

    print(f"\n\tLaptop: Received data from Pi:\n\t\tNumber of Posts:  {max_posts}\n\t\tInterval between recording sessions: {interval_between_scans}\n")

    # close connection socket with the client
    client_socket.close()
    print("\tLaptop: Finished receiving data from client.\n")
    # close server socket
    server.close()
    return max_posts, interval_between_scans

## Sends the image to the pi in chunks
def send_image(filename):
    global CURRENT_PI
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_ip = CURRENT_PI
    port = PI_PORT

    client.connect((client_ip, port))

    file_size = os.path.getsize(filename)
    print(f"\tLaptop: Sending: file_size = {file_size} of the image.")

    # Send the size of the file first
    client.sendall(str(file_size).encode())

    # Wait for acknowledgment from the server before sending the file
    acknowledgment = client.recv(1024)
    if acknowledgment == None:
        print("ERROR: Unable to send file_size to Pi.")
        return 
    
    print(f"\n\tPi: Successfully received file_size\n")

    print(f"\tLaptop: Sending {filename} in chunks of 1024 bytes to the pi.")
    
    with open(filename, 'rb') as file:
        image_data = file.read(1024)
        while image_data:
            client.send(image_data)
            image_data = file.read(1024)

    print("\tLaptop: Image sent successfully.\n")
    client.close()

## Main method for laptop
def main():
    max, interval = laptop.receive_data()
    print("\nExecuting Program...\n")

    i = 1
    while i <= int(max):
        print(f"   Execution cycle : {i} of {max}")
        image = wb.get_vid_net()
        laptop.send_image(image)
        wb.deleteAll()
        time.sleep(int(interval))
        i += 1
    print("\nProgram Completed Execution.\n")