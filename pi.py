import socket
import datetime
import twitter_bot as tb

number_of_posts = 0
max = 0

CSU_IP_PI = "10.84.199.19"
CSU_IP_LAPTOP = "10.84.28.68"
HOME_IP = "10.0.0.232"

def send_data(max_posts, interval_between_scans):
    global max, CSU_IP_LAPTOP
    max = int(max_posts)
    # create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = CSU_IP_LAPTOP  # replace with the server's IP address
    server_port = 1420  # replace with the server's port number

    # establish connection with server
    client.connect((server_ip, server_port))

    while True:
        # input message and send it to the server
        client.send(max_posts.encode("utf-8")[:2048])

        # receive message from the server
        response = client.recv(2048)
        response = response.decode("utf-8")

        # if server sent us "closed" in the payload, we break out of the loop and close our socket
        if response.lower() == "received":
            break
        
    while True:
        client.send(interval_between_scans.encode("utf-8")[:2048])

        # receive message from the server
        response = client.recv(2048)
        response = response.decode("utf-8")

        # if server sent us "closed" in the payload, we break out of the loop and close our socket
        if response.lower() == "received":
            print("Successfully sent data.")
            receive_image()
            break

    # close client socket (connection to the server)
    client.close()
    print("Program completed execution.")

def receive_image():
    global max_posts, number_of_posts, CSU_IP_PI

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = CSU_IP_PI
    port = 1421

    server.bind((server_ip, port))
    server.listen()

    while number_of_posts <= max:
        filename = "image_to_tweet.jpg"

        client_socket, client_address = server.accept()

        # Receive the size of the file first
        file_size = int(client_socket.recv(1024).decode())

        # Send acknowledgment to the client
        client_socket.send(b"ACK")

        with open(filename, "wb") as file:
            received_data = 0
            while received_data < file_size:
                image_chunk = client_socket.recv(1024)
                received_data += len(image_chunk)
                file.write(image_chunk)

        send_tweet(filename)

        if number_of_posts == max:
            client_socket.close()
            break

def send_tweet(filename):
    global number_of_posts
    number_of_posts += 1
    current_time = datetime.datetime.now().strftime("%m/%d/%Y%H:%M:%S")
    tb.tweet_text_and_media(f"""{current_time[0:current_time.find(':') - 2]}
                            \n{current_time[current_time.find(':') - 2:]}
                            \nALERT: Intruder #{number_of_posts}!""",
                            filename)

def main():
    global max_posts
    max_posts = input("Enter max number of posts:  ")
    interval_between_scans = input("Enter amount of time between scans:  ")

    send_data(max_posts, interval_between_scans)

if __name__ == "__main__":
    main()