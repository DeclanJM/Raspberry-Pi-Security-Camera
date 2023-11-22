import socket
import datetime
import twitter_bot as tb

CSU_PI = "10.84.199.19"
CSU_LAPTOP = "10.84.28.68"
HOME_IP = "10.0.0.232"
DENZEL_PI = "172.16.52.120"
DENZEL_LAPTOP = "172.16.52.119"
DAD_LAPTOP = "192.168.1.26"
DAD_PI = "192.168.1.27"

CURRENT_LAPTOP = DAD_LAPTOP
LAPTOP_PORT = 1420
CURRENT_PI = DAD_PI
PI_PORT = 1421

number_of_posts = 0
max = 0

##  Joins laptop server, sends max number of posts and the interval between scans over the socket
def send_data(max_posts, interval_between_scans):
    global max
    max = int(max_posts)

    server_ip = CURRENT_LAPTOP
    server_port = LAPTOP_PORT

    #  Creates a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #  Establish connection with server
    client.connect((server_ip, server_port))

    while True:
        #  Input message and send it to the server
        client.send(max_posts.encode("utf-8")[:2048])

        #  Receive message from the server
        response = client.recv(2048).decode("utf-8")

        #  If the server responded with "received" then we have successfully sent the max_posts variable
        if response.lower() == "received":
            print(f"\n\tLaptop: Successfully recieved max_posts = {max_posts}")
            break
        
    while True:
        client.send(interval_between_scans.encode("utf-8")[:2048])

        #  Receive message from the server
        response = client.recv(2048).decode("utf-8")  #  Convert bytes to string

        #  If the server responded with "received" then we have successfully sent the interval_between_scans variable
        if response.lower() == "received":
            print(f"\tLaptop: Successfully recieved interval_between_scans = {interval_between_scans}\n")
            print("\tPi: Closing connection and waiting to receive image from Laptop...\n")
            
            client.close() #  Close client socket (connection to the server)
            receive_image()
            break

    print("Program Completed Execution.\n")

##  Creates a new socket, waits for the laptop to join, and then downloads the image in chunks from the laptop
def receive_image():
    ##AF_INET means we are connecting using IP, SOCK_STREAM means we are transmitting using TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = CURRENT_PI
    port = PI_PORT

    #  Bind the socket to a specific IP and Port and listen for new connections
    server.bind((server_ip, port))
    server.listen()
    print(f"\tPi: Server Initialized. Listening on {server_ip}:{port}")

    

    #  Receive an image and post it to twitter until number_of_posts == max
    while number_of_posts <= max:
        filename = "image_to_tweet.jpg"

        #  Accept incoming connections
        client_socket, client_address = server.accept()
        print(f"\tPi: Accepted connection from {client_address[0]}:{client_address[1]}\n")
        print("Receiving image data now...\n")

        #  Receive the size of the file first
        file_size = int(client_socket.recv(1024).decode())
        print(f"\tPi: Received file_size = {file_size} bytes from Laptop @ {client_address}")

        #  Send acknowledgment back to the client
        client_socket.send(b"ACK")

        print("\tPi: Receiving image chunks 1024 bytes at a time...")
        with open(filename, "wb") as file:  #  Receive data in chunks of 1024 bytes until the Pi has received the entire image, builds the image from top to bottom
            received_data = 0
            while received_data < file_size:
                image_chunk = client_socket.recv(1024)
                received_data += len(image_chunk)
                file.write(image_chunk)
        print("\tPi: Image received, posting to Twitter...")

        send_tweet(filename)

        if number_of_posts == max:
            client_socket.close()
            break

##  Sends the new downloaded image file to twitter_bot to be posted
def send_tweet(filename):
    global number_of_posts
    number_of_posts += 1
    current_time = datetime.datetime.now().strftime("%m/%d/%Y%H:%M:%S")
    tb.tweet_text_and_media(f"""{current_time[0:current_time.find(':') - 2]}
                            \n{current_time[current_time.find(':') - 2:]}
                            \nALERT: Intruder #{number_of_posts}!""",
                            filename)

##  Main method for the Raspberry Pi
def main():
    max_posts = input("Enter max number of posts:  ")
    interval_between_scans = input("Enter amount of time between scans:  ")

    send_data(max_posts, interval_between_scans)