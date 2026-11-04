import cv2
import pygame
import os
import glob
import socket
import threading
import time
from ffpyplayer.player import MediaPlayer

VIDEO_DIR = os.path.join(os.path.dirname(__file__), "..", "videos")
LISTEN_PORT = 5555

video_trigger = threading.Event()
current_video_index = 0
video_files = []

def get_video_files():
    """Get all video files sorted by part number"""
    global video_files
    video_files = glob.glob(os.path.join(VIDEO_DIR, "part*.mp4"))
    video_files.sort()
    return video_files

def listen_for_ev3():
    """Listen for signals from EV3 brick"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', LISTEN_PORT))
    print(f"Listening for EV3 signals on port {LISTEN_PORT}...")
    
    while True:
        data, addr = sock.recvfrom(1024)
        if data == b"START_VIDEO":
            print(f"Received START_VIDEO signal from {addr}")
            video_trigger.set()
        elif data == b"NEXT_VIDEO":
            print(f"Received NEXT_VIDEO signal from {addr}")
            video_trigger.set()

def play_video_sequence():
    """Play videos in sequence with EV3 button control"""
    global current_video_index
    
    pygame.init()
    
    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption("Video Player")
    
    screen.fill((0, 0, 0))
    pygame.display.flip()
    
    video_files = get_video_files()
    print(f"Found {len(video_files)} videos")
    print("Waiting for RIGHT_DOWN button on EV3 remote...")
    
    current_video_index = 0
    
    video_trigger.wait()
    video_trigger.clear()
    
    while current_video_index < len(video_files):
        video_path = video_files[current_video_index]
        print(f"Playing video {current_video_index + 1}/{len(video_files)}: {os.path.basename(video_path)}")
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error opening video: {video_path}")
            current_video_index += 1
            continue
        
        audio_player = MediaPlayer(video_path)
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0:
            fps = 30
        
        last_frame = None
        clock = pygame.time.Clock()
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            audio_frame, audio_val = audio_player.get_frame()
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            last_frame = frame.copy()
            
            h, w = frame.shape[:2]
            scale = min(screen_width / w, screen_height / h)
            new_w = int(w * scale)
            new_h = int(h * scale)
            frame = cv2.resize(frame, (new_w, new_h))
            
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            
            x = (screen_width - new_w) // 2
            y = (screen_height - new_h) // 2
            
            screen.fill((0, 0, 0))
            screen.blit(frame_surface, (x, y))
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cap.release()
                    audio_player.close_player()
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        cap.release()
                        audio_player.close_player()
                        pygame.quit()
                        return
            
            clock.tick(fps)
        
        cap.release()
        audio_player.close_player()
        
        if last_frame is not None and current_video_index < len(video_files) - 1:
            h, w = last_frame.shape[:2]
            scale = min(screen_width / w, screen_height / h)
            new_w = int(w * scale)
            new_h = int(h * scale)
            last_frame = cv2.resize(last_frame, (new_w, new_h))
            frame_surface = pygame.surfarray.make_surface(last_frame.swapaxes(0, 1))
            
            x = (screen_width - new_w) // 2
            y = (screen_height - new_h) // 2
            
            screen.fill((0, 0, 0))
            screen.blit(frame_surface, (x, y))
            pygame.display.flip()
            
            print(f"Video ended. Showing last frame. Press RIGHT_DOWN to continue...")
            
            video_trigger.wait()
            video_trigger.clear()
        
        current_video_index += 1
    
    print("All videos complete. Showing final frame. Press ESC to exit.")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
        pygame.time.wait(100)
    
    pygame.quit()

if __name__ == "__main__":
    listener_thread = threading.Thread(target=listen_for_ev3, daemon=True)
    listener_thread.start()
    
    print("PC Video Player Ready")
    print("Press RIGHT_DOWN on EV3 remote to start/advance videos")
    print("Press ESC to exit")
    
    play_video_sequence()
