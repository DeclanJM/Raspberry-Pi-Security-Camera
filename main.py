import time
import webcam
import laptop
import pi


# Runs entire program in one window locally, does not use sockets at all
def main_local():
    max_posts = int(input("Enter max number of posts:  "))
    interval_between_scans = int(input("Enter amount of time between scans:  "))
    
    print("Starting program...\n")

    i = 1
    while i <= max_posts:
        webcam.get_vid(i)
        time.sleep(interval_between_scans)
        i += 1


# Uses sockets to communicate and run the program between the laptop and raspberry Pi
def main():
    machine = input("\nWhich machine are you running on?\n    Raspberry Pi or Laptop\n\t(P or L):  ")
    if machine.lower() == "l":
        laptop.main()
    elif machine.lower() == "p":
        pi.main()
    else:
        print("Invalid Option.")
        main()


if __name__ == "__main__":
    # Runs both sides of the program locally
    #main_local()

    # Runs the program between pi and laptop
    main()
