import time
import webcam
import laptop
import pi

def main_loop():
    max_posts = int(input("Enter max number of posts:  "))
    interval_between_scans = int(input("Enter amount of time between scans:  "))
    
    print("Starting program...\n")

    i = 1
    while i <= max_posts:
        webcam.get_vid(i)
        time.sleep(interval_between_scans)
        i += 1

def main():
    machine = input("Which machine are you running on?\nRaspberry Pi or Laptop?\n\t(P or L):  ")
    if machine.lower() == "l":
        laptop.main()
    elif machine.lower() == "p":
        pi.main()
    else:
        print("Invalid Option.\nGoodbye!")

if __name__ == "__main__":
    #main_loop()        ##Runs entire program locally
    main()              ##Runs program split between pi and laptop