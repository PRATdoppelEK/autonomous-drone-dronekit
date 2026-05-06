"""
camera_feed.py
--------------
Capture and display live camera feed from the drone.
Save images on demand by pressing 's'. Press 'q' to quit.

Usage:
    python camera_feed.py

Note:
    Replace VideoCapture(0) with the drone's RTSP/UDP stream URL
    when using real hardware, e.g.:
    cap = cv2.VideoCapture('rtsp://192.168.1.1:554/stream')
"""

import cv2
import time
import os


def capture_camera_feed(source=0, save_dir='captured_images'):
    """
    Display live camera feed and allow image saving.

    Args:
        source: Camera source. 0 for webcam, or RTSP URL string for drone stream.
        save_dir (str): Directory to save captured images.
    """
    os.makedirs(save_dir, exist_ok=True)

    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print(f"Error: Could not open camera source: {source}")
        return

    print("Camera feed active.")
    print("  Press 's' to save image")
    print("  Press 'q' to quit")

    frame_count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Warning: Failed to read frame. Retrying...")
            time.sleep(0.1)
            continue

        # Overlay timestamp on frame
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, timestamp, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow('Drone Camera Feed', frame)
        frame_count += 1

        key = cv2.waitKey(1) & 0xFF

        # Save image
        if key == ord('s'):
            filename = os.path.join(save_dir, f"frame_{frame_count}_{int(time.time())}.jpg")
            cv2.imwrite(filename, frame)
            print(f"Image saved: {filename}")

        # Quit
        elif key == ord('q'):
            print("Exiting camera feed.")
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Use source=0 for webcam simulation
    # Replace with RTSP stream URL for real drone hardware
    capture_camera_feed(source=0)
