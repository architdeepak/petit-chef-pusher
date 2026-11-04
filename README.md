# Petit Chef Pusher

EV3 MicroPython motor control and a companion PC video player for a Le Petit Chef-inspired dinner setup.

## EV3 controller

`main.py` runs on an EV3 brick with Pybricks EV3 MicroPython, not desktop Python.

- Motors connect to ports A, B, and C.
- An infrared sensor connects to S1 and listens on remote channel 1.
- Right Up runs motor A forward and back.
- Left Up runs motor B in reverse and back.
- Left Down runs motor C forward and back.
- Right Down sends `START_VIDEO` to the PC over UDP port 5555.

Set `PC_IP` in `main.py` to the PC's local address. Review motor speed and duration constants for your mechanism and clear the mechanism before running it: this code physically moves motors.

## PC video player

Use desktop Python with the EV3 and PC on a network that allows UDP port 5555:

```powershell
python -m pip install -r requirements.txt
python pc_video_player.py
```

Place your own `part*.mp4` files in a sibling `videos/` directory, one level above this project folder. Files are sorted by filename; use zero-padded numbers if you have more than ten parts. Playback starts when the EV3 sends its remote-button signal.

Video assets are not included. Review the existing personal speaker greeting in `main.py` before using the controller for another event.
