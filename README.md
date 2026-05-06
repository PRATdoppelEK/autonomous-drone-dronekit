# Autonomous Drone Programming with DroneKit & Python

A Python-based project for programming and controlling autonomous unmanned aerial vehicles (UAVs) using DroneKit and OpenCV. This project grew out of my Bachelor's thesis at Rajasthan Technical University, where I designed and analysed a Quadcopter (UAV) and a compressed-air vehicle (CRAVE). The hands-on engineering work sparked a deeper interest in autonomous flight systems — this repository documents that continued exploration.

---

## Project Overview

This project covers the full control lifecycle of an autonomous drone:

- Connecting to a drone (simulation or real hardware via MAVLink)
- Arming, taking off, and landing autonomously
- GPS-based waypoint navigation
- Live camera feed integration
- Real-time obstacle detection using computer vision
- Object tracking with OpenCV
- Safe return-to-launch (RTL) procedures

The code is written for both **simulation** (via MAVProxy / SITL) and **real hardware** deployment, making it easy to test safely before flying.

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.8+ | Primary language |
| DroneKit | MAVLink-based drone communication & control |
| OpenCV | Computer vision, camera feed, object tracking |
| MAVProxy / SITL | Simulation environment |
| NumPy | Image processing support |

---

## Project Structure

```
autonomous-drone-dronekit/
│
├── README.md
├── requirements.txt
│
├── connection.py          # Connect to drone, read telemetry
├── arm_takeoff.py         # Arm vehicle and execute takeoff sequence
├── navigation.py          # GPS waypoint navigation
├── camera_feed.py         # Live camera stream capture and image saving
├── obstacle_detection.py  # Edge-based obstacle detection with OpenCV
├── object_tracking.py     # Real-time object tracking (MOSSE tracker)
├── return_to_launch.py    # RTL and auto-land procedures
│
├── examples/
│   ├── full_mission.py    # Complete autonomous mission example
│   └── simulation_test.py # SITL simulation test script
│
├── tests/
│   └── test_navigation.py # Unit tests for navigation logic
│
└── docs/
    └── setup.md           # Setup guide for simulation and hardware
```

---

## Getting Started

### Prerequisites

```bash
pip install dronekit opencv-python numpy pymavlink
```

For simulation (SITL):
```bash
pip install dronekit-sitl
```

### Run in Simulation

```bash
# Start SITL simulation
dronekit-sitl copter --home=47.397742,8.545594,584,353

# In a separate terminal, run your script
python connection.py
```

### Connect to Real Hardware

Change the connection string in any script:

```python
# Simulation
vehicle = connect('127.0.0.1:14550', wait_ready=True)

# Real drone via USB/telemetry
vehicle = connect('/dev/ttyUSB0', baud=57600, wait_ready=True)

# Real drone via UDP
vehicle = connect('udp:192.168.1.1:14550', wait_ready=True)
```

---

## Features

### 1. Connection & Telemetry
Read GPS coordinates, battery level, flight mode, and system status in real time.

### 2. Arm & Takeoff
Automated safety checks before arming. Altitude confirmation before proceeding.

### 3. GPS Waypoint Navigation
Navigate to specific GPS coordinates at a defined altitude using `simple_goto`.

### 4. Camera Integration
Capture and display live drone camera feed. Save images on demand.

### 5. Obstacle Detection
Edge detection via OpenCV Canny algorithm to identify obstacles in camera feed.

### 6. Object Tracking
MOSSE tracker for real-time object selection and tracking. Foundation for follow-me or target-lock functionality.

### 7. Return to Launch / Auto-Land
Safe RTL mode and autonomous landing with vehicle shutdown.

---

## Background & Motivation

During my B.Tech. in Mechanical Engineering, I designed and tested a Quadcopter UAV as part of my final year project — covering aerodynamic analysis, structural design, and flight mechanics. That project showed me how much engineering goes into making something fly reliably.

This repository is the software side of that interest: learning how to command, navigate, and give autonomous perception capabilities to a UAV using Python. It bridges mechanical understanding with software control — the same integration that matters in real-world autonomous systems.

---

## Future Work

- [ ] Integration with ArduPilot Mission Planner for complex mission planning
- [ ] YOLO-based object detection for improved accuracy
- [ ] Geofencing implementation
- [ ] Multi-drone coordination (swarm basics)
- [ ] ROS integration for advanced autonomy

---

## Author

**Prateek Gaur**
M.Sc. Energy Engineering – TU Berlin
B.Tech. Mechanical Engineering – Rajasthan Technical University

[Portfolio](https://prateek-gaur-ml-bz0s69q.gamma.site/) | [GitHub](https://github.com/PRATdoppelEK)
