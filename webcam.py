import cv2
import time
import datetime
import os
import shutil
import twitter_bot as tb


SECONDS_TO_RECORD_AFTER_DETECTION = 2  # Amount of time after a face stopped being detected before the camera ends the recording
CAMERA_ID = 0  # 0 is default webcam: ~5s startup, 1 is usb webcam: ~60s startup
VIDEO_REPLAY = False  #True if you want to display the frame-by-frame replay of the footage (Slows program down considerably)


# Webcam starts recording when it detects a face, then stops after a 3 second period of not seeing one, then calls the get_img function
def get_vid(number_of_posts):
    global SECONDS_TO_RECORD_AFTER_DETECTION, CAMERA_ID

    detection = False
    timer_started = False
    first_sight = True
    detection_stopped_time = None

    vidCap = cv2.VideoCapture(CAMERA_ID)   

    face_data = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    body_data = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_fullbody.xml")

    frame_size = (int(vidCap.get(3)), int(vidCap.get(4)))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    run = True

    while run:
        if not os.path.exists("video"):
            os.makedirs("video") 

        _, frame = vidCap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_data.detectMultiScale(gray, 1.3, 5)
        bodies = body_data.detectMultiScale(gray, 1.3, 5)

        if len(faces) + len(bodies) > 0:
            if detection:
                if first_sight:
                    print("\nFace Detected: Recording Started!")
                    first_sight = False

                timer_started = False
            else:
                detection = True
                current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
                filename = f"video/{current_time}.mp4"
                out = cv2.VideoWriter(filename, fourcc, 20, frame_size)

        elif detection:
            if timer_started:
                if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                    out.release()
                    vidCap.release()
                    cv2.destroyAllWindows()
                    print("Detection Lost: Stopped Recording!\n")
                    time.sleep(0.5)
                    print("Tweeting...\n")
                    get_img(filename, number_of_posts)
                    deleteAll()
                    return
                
            else:
                timer_started = True
                detection_stopped_time = time.time()

        if detection:
            for (x, y, width, height) in faces:
                image = cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 0, 255), 3)
                cv2.putText(image, 'INTRUDER!', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            out.write(frame)

        cv2.imshow("Camera", frame)

        if cv2.waitKey(1) == ord('q'):
            out.release()
            vidCap.release()
            cv2.destroyAllWindows()
            break


# Replays each frame of the video and returns the one in the middle to be posted on twitter
def get_img(filename, number_of_posts):
    global SECONDS_TO_RECORD_AFTER_DETECTION, VIDEO_REPLAY

    if not os.path.exists("frames"):
        os.makedirs("frames")
    
    vid = cv2.VideoCapture(filename)

    total_frames = vid.get(cv2.CAP_PROP_FRAME_COUNT) 
    fps = vid.get(cv2.CAP_PROP_FPS) 
    current_frame = 0
    remove_frame = SECONDS_TO_RECORD_AFTER_DETECTION * fps  # Number of frames after the face stopped being detected
    return_frame = round((total_frames - remove_frame) / 2)

    while True:
        success, frame = vid.read()

        if VIDEO_REPLAY:
            cv2.imshow("Video Replay", frame)

        if (current_frame == return_frame) and (current_frame > 2):
            cv2.imwrite("frames/" + str(current_frame) + ".jpg", frame)
            cv2.destroyAllWindows()
            current_time = datetime.datetime.now().strftime("%m/%d/%Y%H:%M:%S")
            tb.tweet_text_and_media(f"""{current_time[0:current_time.find(':') - 2]}
                                    \n{current_time[current_time.find(':') - 2:]}
                                    \nALERT: Intruder #{number_of_posts}!""",
                                    f"frames/{str(return_frame)}.jpg")
            return

        else:
            current_frame += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q' is the exit key to end the program
            vid.release()
            cv2.destroyAllWindows()
            return


# Cleans up filesystem so there aren't tens of videos and hundreds of frames
def deleteAll():
    video_folder = "./video"
    frames_folder = "./frames"
    shutil.rmtree(frames_folder, ignore_errors = True)
    shutil.rmtree(video_folder, ignore_errors = True)

# get_vid but for over the network, returns the filename 
def get_vid_net():
    global SECONDS_TO_RECORD_AFTER_DETECTION, CAMERA_ID

    detection = False
    timer_started = False
    first_sight = True
    detection_stopped_time = None

    vidCap = cv2.VideoCapture(CAMERA_ID)

    face_data = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    body_data = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_fullbody.xml")


    frame_size = (int(vidCap.get(3)), int(vidCap.get(4)))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    run = True

    while run:
        if not os.path.exists("video"):
            os.makedirs("video") 

        _, frame = vidCap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_data.detectMultiScale(gray, 1.3, 5)
        bodies = body_data.detectMultiScale(gray, 1.3, 5)

        if len(faces) + len(bodies) > 0:
            if detection:
                if first_sight:
                    print("\n\tWebcam: Face Detected. Recording Started!")
                    first_sight = False

                timer_started = False

            else:
                detection = True
                current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
                filename = f"video/{current_time}.mp4"
                out = cv2.VideoWriter(filename, fourcc, 20, frame_size)

        elif detection:
            if timer_started:
                if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                    out.release()
                    vidCap.release()
                    cv2.destroyAllWindows()
                    print("\tWebcam: Detection Lost. Stopped Recording!\n")
                    time.sleep(0.5)
                    return get_img_net(filename)
                
            else:
                timer_started = True
                detection_stopped_time = time.time()

        if detection:
            for (x, y, width, height) in faces:
                image = cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 0, 255), 3)
                cv2.putText(image, 'INTRUDER!', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            out.write(frame)

        cv2.imshow("Camera", frame)

        if cv2.waitKey(1) == ord('q'):
            out.release()
            vidCap.release()
            cv2.destroyAllWindows()
            break

# get_img but for over the network
def get_img_net(filename):
    global SECONDS_TO_RECORD_AFTER_DETECTION, VIDEO_REPLAY

    if not os.path.exists("frames"):
        os.makedirs("frames")
    
    vid = cv2.VideoCapture(filename)

    total_frames = vid.get(cv2.CAP_PROP_FRAME_COUNT) 
    fps = vid.get(cv2.CAP_PROP_FPS) 
    current_frame = 0
    remove_frame = SECONDS_TO_RECORD_AFTER_DETECTION * fps  # Number of frames after the face stopped being detected
    return_frame = round((total_frames - remove_frame) / 2)

    while True:
        success, frame = vid.read()

        if VIDEO_REPLAY:
            cv2.imshow("Video Replay", frame)

        if (current_frame == return_frame) and (current_frame > 2):
            cv2.imwrite("frames/" + str(current_frame) + ".jpg", frame)
            cv2.destroyAllWindows()
            return f"frames/{str(return_frame)}.jpg"

        else:
            current_frame += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q' is the exit key to end the program
            vid.release()
            cv2.destroyAllWindows()
            return
        