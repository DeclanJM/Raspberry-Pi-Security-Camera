import time
import webcam as wb
import twitter_bot as tb

def record_loop(max_posts, interval_between_scans):
    thread_id = tb.start_thread("New Security Camera Session Starting...")
    for i in max_posts:
        wb.get_vid(thread_id, i)
        time.sleep(interval_between_scans)

if __name__ == "__main__":
    max_posts = input("Enter max number of posts:  ")
    interval_between_scans = input("Enter amount of time between scans:  ")
    record_loop(max_posts, interval_between_scans)