# CS370 Practical Project: Raspberry Pi - Security Camera - Twitter Bot

## Instructions

1. Use the ***pip3 install requirements.txt*** command on your laptop, no need to do this for the pi.
2. Create your own Twitter/X bot account following the steps in this video: ***https://youtu.be/2UBcRiddwAo?si=BjO9CFjqJShcDUZf&t=60***
3. Input your API tokens into the oauth2.py file.
4. Use the ***ipconfig*** command in CMD/Terminal on your laptop, and copy the ipv4 address under ***'Wireless LAN adapter: WiFi'*** and paste it into the ***HOME_LAPTOP*** variable in both pi.py and laptop.py.
5. Use the ***ifconfig*** command in Terminal on your Pi, and copy the WiFi inet address and paste it into the ***HOME_PI*** variable in both pi.py and laptop.py.
6. If you are working in multiple locations, you can have multiple IPs saved, just make sure you adjust the ***CURRENT_LAPTOP*** and ***CURRENT_PI*** variables in both those files.
7. Change ***CAMERA_ID*** in the webcam.py file to either be 0 for default, or 1 for a usb webcam.
8. Play around with other global variables' values: ***SECONDS_TO_RECORD_AFTER_DETECTION*** or ***VIDEO_REPLAY*** in webcam.py.
9. Use the ***python3 main.py*** command on both the laptop and the pi.
10. Give the ***laptop input first***, that way it can create the server socket.
11. Give the ***pi input second***, determining the max number of posts and the time in seconds between posts in which the program will wait.
12. Let the program run, if you need to crash it, use CTRL+C in the terminal or 'q' on the Camera window.