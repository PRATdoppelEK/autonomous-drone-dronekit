"""
object_tracking.py
------------------
Real-time object tracking using OpenCV MOSSE tracker.
Select a region of interest (ROI) and the tracker follows it.
Foundation for follow-me or target-lock drone behaviour.

Usage:
    python object_tracking.py

Controls:
    - On launch: draw a box around the object to track, then press ENTER or SPACE
    - Press 'r' to reset and select a new target
    - Press 'q' to quit
"""

import cv2
import time


def track_object(source=0):
    """
    Track a selected object in real-time using MOSSE tracker.

    Args:
        source: Camera source (0 for webcam, or RTSP URL for drone stream).
    """
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print(f"Error: Could not open camera source: {source}")
        return

    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read initial frame.")
        cap.release()
        return

    print("Object Tracking active.")
    print("  Draw a box around the object to track, then press ENTER or SPACE.")
    print("  Press 'r' to re-select target | 'q' to quit.")

    # Initialise MOSSE tracker (fast and lightweight — good for embedded systems)
    tracker = cv2.legacy.TrackerMOSSE_create()

    # Let user select ROI
    bbox = cv2.selectROI('Object Tracking', frame, fromCenter=False, showCrosshair=True)
    tracker.init(frame, bbox)
    tracking = True

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Warning: Frame read failed.")
            time.sleep(0.1)
            continue

        if tracking:
            success, bbox = tracker.update(frame)

            if success:
                x, y, w, h = [int(v) for v in bbox]

                # Draw tracking box
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Calculate centre of tracked object
                cx, cy = x + w // 2, y + h // 2
                cv2.circle(frame, (cx, cy), 4, (0, 255, 0), -1)

                # Show centre coordinates (useful for sending motion commands)
                cv2.putText(frame, f"Target: ({cx}, {cy})", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                status = "TRACKING"
                color = (0, 255, 0)

                # --- Motion command hook ---
                # Here you would calculate the offset from frame centre
                # and send corresponding velocity commands to the drone:
                #
                # frame_cx = frame.shape[1] // 2
                # frame_cy = frame.shape[0] // 2
                # offset_x = cx - frame_cx
                # offset_y = cy - frame_cy
                # send_velocity_command(vehicle, offset_x, offset_y)

            else:
                status = "TARGET LOST"
                color = (0, 0, 255)
                cv2.putText(frame, "TARGET LOST", (75, 75),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            cv2.putText(frame, status, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        cv2.imshow('Object Tracking', frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            print("Exiting tracker.")
            break
        elif key == ord('r'):
            print("Re-selecting target...")
            ret, frame = cap.read()
            tracker = cv2.legacy.TrackerMOSSE_create()
            bbox = cv2.selectROI('Object Tracking', frame,
                                  fromCenter=False, showCrosshair=True)
            tracker.init(frame, bbox)
            tracking = True

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    track_object(source=0)
