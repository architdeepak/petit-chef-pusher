# Petit Chef Pusher

An EV3 remote moves three motors and starts a video on a nearby PC. The brick runs Pybricks EV3 MicroPython. The PC player uses OpenCV, Pygame and FFpyPlayer.

Connect the motors to A, B and C and the infrared sensor to S1. Set `PC_IP` in `main.py` to the PC's local address, then run the script on the brick. On remote channel 1, Right Up moves A, Left Up moves B and Left Down moves C. Right Down tells the PC to start playback over UDP port 5555.

On the PC, run:

```sh
python -m pip install -r requirements.txt
python pc_video_player.py
```

Put your own `part*.mp4` files in a `videos` folder next to the project folder. The player sorts them by filename, so use names like `part01.mp4` and `part02.mp4`.
