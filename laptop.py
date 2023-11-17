import socket
import os
import laptop
import webcam as wb
import time

CSU_IP_PI = "10.84.199.19"
CSU_IP_LAPTOP = "10.84.28.68"
HOME_IP = "10.0.0.232"
DENZEL_PI = "172.16.52.120"
DENZEL_LAPTOP = "172.16.52.119 "

def receive_data():
    # create a socket object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    global CSU_IP_LAPTOP, DENZEL_LAPTOP

    server_ip = DENZEL_LAPTOP #CSU_IP_LAPTOP
    port = 1420

    # bind the socket to a specific address and port
    server.bind((server_ip, port))
    # listen for incoming connections
    server.listen(0)
    print(f"Listening on {server_ip}:{port}")

    # accept incoming connections
    client_socket, client_address = server.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}\n")
    print("Receiving data now...")

    # receive data from the client
    while True:
        max_posts = client_socket.recv(2048)
        max_posts = max_posts.decode("utf-8") # convert bytes to string

        client_socket.send("received".encode("utf-8"))
        break

    while True:
        interval_between_scans = client_socket.recv(2048)
        interval_between_scans = interval_between_scans.decode("utf-8")

        client_socket.send("received".encode("utf-8"))
        break

    print(f"\nReceived Data:\n\tNumber of Posts:  {max_posts}\n\tInterval between recording sessions: {interval_between_scans}\n")

    # close connection socket with the client
    client_socket.close()
    print("Finished receiving data from client.\n")
    # close server socket
    server.close()
    return max_posts, interval_between_scans

def send_image(filename):
    global CSU_IP_PI, DENZEL_PI
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_ip = DENZEL_PI #CSU_IP_PI
    port = 1421

    client.connect((client_ip, port))

    file_size = os.path.getsize(filename)
    print(f"Sending: file_size = {file_size} of the image.")

    # Send the size of the file first
    client.sendall(str(file_size).encode())

    # Wait for acknowledgment from the server before sending the file
    acknowledgment = client.recv(1024)
    if acknowledgment == None:
        print("Error sending file_size to client.")
        return 
    
    print(f"Client successfully received file_size\n")

    print(f"Sending: {filename} in chunks to pi.")
    
    with open(filename, 'rb') as file:
        image_data = file.read(1024)
        while image_data:
            client.send(image_data)
            image_data = file.read(1024)

    print("Image sent successfully\n")
    client.close()

def main():
    max, interval = laptop.receive_data()
    print("\nExecuting Program...\n")

    i = 1
    while i <= int(max):
        image = wb.get_vid_net()
        laptop.send_image(image)
        time.sleep(int(interval))
        i += 1
        wb.deleteAll()