import time
import webcam as wb

def main():
    max_posts = int(input("Enter max number of posts:  "))
    interval_between_scans = int(input("Enter amount of time between scans:  "))
    
    print("Starting program...\n")

    i = 1
    while i <= max_posts:
        wb.get_vid(i)
        time.sleep(interval_between_scans)
        i += 1

if __name__ == "__main__":
    main()