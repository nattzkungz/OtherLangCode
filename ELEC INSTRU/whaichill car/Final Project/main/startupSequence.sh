libcamera-vid -t0 --width 1920 --height 1080 --framerate 30 --nopreview --codec h264 --profile high --intra 5 --listen -o tcp://0.0.0.0:8494

python3 main.py