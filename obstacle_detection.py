"""
obstacle_detection.py
---------------------
Real-time obstacle detection using OpenCV edge detection.
Processes live camera feed and highlights potential obstacles.

Usage:
    python obstacle_detection.py

Note:
    Replace VideoCapture(0) with drone camera stream URL for real hardware.
"""

import cv2
import numpy as np
import time


def detect_obstacles(source=0, canny_low=50, canny_high=150,
                     min_contour_area=500):
    """
    Detect obstacles in camera feed using Canny edge detection and contour analysis.

    Args:
        source: Camera source (0 for webcam, or RTSP URL).
        canny_low (int): Lower threshold for Canny edge detector.
        canny_high (int): Upper threshold for Canny edge detector.
        min_contour_area (int): Minimum contour area to flag as obstacle.
    """
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print(f"Error: Could not open camera source: {source}")
        return

    print("Obstacle detection active. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Warning: Frame read failed.")
            time.sleep(0.1)
            continue

        # Convert to grayscale for edge detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Canny edge detection
        edges = cv2.Canny(blurred, canny_low, canny_high)

        # Find contours from edges
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)

        obstacle_count = 0

        for contour in contours:
            area = cv2.contourArea(contour)

            if area > min_contour_area:
                # Draw bounding box around detected obstacle
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, f"Obstacle ({int(area)}px)",
                            (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 0, 255), 1)
                obstacle_count += 1

        # Status overlay
        status_text = f"Obstacles detected: {obstacle_count}"
        color = (0, 0, 255) if obstacle_count > 0 else (0, 255, 0)
        cv2.putText(frame, status_text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        # Show both original (with annotations) and edge map
        cv2.imshow('Obstacle Detection', frame)
        cv2.imshow('Edge Map', edges)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting obstacle detection.")
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    detect_obstacles(source=0)
