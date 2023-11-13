import cv2
import time
import datetime
import os
import shutil
import twitter_bot as tb


def get_vid(number_of_posts):
    cap = cv2.VideoCapture(0)   ##0 is default webcam: 5s startup, 1 is logi: 63s startup

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    body_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_fullbody.xml")

    detection = False
    detection_stopped_time = None
    timer_started = False
    SECONDS_TO_RECORD_AFTER_DETECTION = 3

    frame_size = (int(cap.get(3)), int(cap.get(4)))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    run = True

    while run:
        if not os.path.exists("videos"):
            os.makedirs("videos") 

        _, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        bodies = body_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) + len(bodies) > 0:
            if detection:
                timer_started = False
            else:
                detection = True
                current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
                filename = f"videos/{current_time}.mp4"
                out = cv2.VideoWriter(filename, fourcc, 20, frame_size)
                print("Started Recording!")
        elif detection:
            if timer_started:
                if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                    detection = False
                    timer_started = False
                    out.release()
                    cv2.destroyAllWindows()
                    run = False
                    print('Stopped Recording!')
                    get_img(filename, number_of_posts)
                    deleteAll()
            else:
                timer_started = True
                detection_stopped_time = time.time()

        if detection:
            out.write(frame)

        for (x, y, width, height) in faces:
            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 0, 255), 3)

        cv2.imshow("Camera", frame)

        if cv2.waitKey(1) == ord('q'):
            break

    out.release()
    cap.release()
    cv2.destroyAllWindows()

def get_img(filename, number_of_posts):
    if not os.path.exists("vid_frames"):
        os.makedirs("vid_frames")
    
    vid = cv2.VideoCapture(filename)
    currentFrame = 0

    while True:
        success, frame = vid.read()

        if success != True and currentFrame > 2:
            cv2.destroyAllWindows()
            tb.tweet(f"ALERT: Intruder #{number_of_posts}!", "vid_frames/" + str(int((currentFrame)/2)) + ".jpg")
            currentFrame = 0
            break

        face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, width, height) in faces:
            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 0, 255), 3)

        cv2.imshow("Video Replay", frame)
        cv2.imwrite("vid_frames/" + str(currentFrame) + ".jpg", frame)
        currentFrame += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    vid.release()
    cv2.destroyAllWindows()

def deleteAll():
    vid_folder = "./videos"
    vid_frames_folder = "./vid_frames"
    shutil.rmtree(vid_frames_folder, ignore_errors = True)
    shutil.rmtree(vid_folder, ignore_errors = True)