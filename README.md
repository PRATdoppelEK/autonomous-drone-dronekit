# Autonomous Drone Control — DroneKit & Python

> MAVLink-based autonomous UAV control stack with real-time computer vision, GPS waypoint navigation, obstacle detection, and object tracking. Deployable on both SITL simulation and real hardware.

---

## What This Is

A modular Python framework for programming autonomous UAV behaviour — from low-level MAVLink communication and flight control, through to real-time perception using OpenCV. The system covers the full mission lifecycle: connect → arm → take off → navigate → perceive → track → return safely.

Written to run on **both simulation (SITL/MAVProxy) and real hardware**, with a clean separation between flight control logic and perception modules.

---

## Why It Exists

My B.Tech. final year project at Rajasthan Technical University involved designing, structurally analysing, and test-flying a Quadcopter UAV — covering aerodynamics, frame design, motor sizing, and basic flight mechanics. That work gave me a solid hardware intuition for what autonomous systems need to do reliably in the real world.

This repository is the software continuation of that: building the perception and control stack that turns a flying platform into an autonomous system. The combination of mechanical understanding and software control is exactly what matters when hardware has to work under real conditions.

---

## System Architecture

```
autonomous-drone-dronekit/
│
├── connection.py           # MAVLink connection, telemetry monitoring
├── arm_takeoff.py          # Pre-arm safety checks, takeoff sequence
├── navigation.py           # GPS waypoint navigation (simple_goto)
├── camera_feed.py          # Live camera stream, frame capture
├── obstacle_detection.py   # Edge-based obstacle detection (Canny/OpenCV)
├── object_tracking.py      # Real-time MOSSE tracker — target lock
├── return_to_launch.py     # RTL mode, auto-land, vehicle shutdown
│
├── examples/
│   ├── full_mission.py     # End-to-end autonomous mission demo
│   └── simulation_test.py  # SITL test script
│
├── docs/
│   └── setup.md            # Hardware + simulation setup guide
│
└── requirements.txt
```

---

## Tech Stack

| Component | Tool |
|-----------|------|
| Language | Python 3.8+ |
| Flight control / MAVLink | DroneKit |
| Computer vision | OpenCV |
| Simulation | DroneKit-SITL / MAVProxy / ArduCopter |
| Telemetry protocol | MAVLink (UDP / USB / telemetry radio) |
| Numerical processing | NumPy |

---

## Core Modules

### Connection & Telemetry — `connection.py`
Establishes MAVLink link to vehicle (simulation or hardware). Streams GPS position, altitude, battery state, flight mode, and armed status in real time. Handles reconnection on link loss.

### Arm & Takeoff — `arm_takeoff.py`
Runs pre-arm safety checks (GPS fix, battery, mode), switches to GUIDED mode, arms motors, and climbs to target altitude with confirmation before proceeding. Altitude verified before handing off to navigation.

### GPS Waypoint Navigation — `navigation.py`
Navigates to absolute GPS coordinates at defined altitude using `simple_goto`. Monitors distance-to-target and triggers next waypoint or action on arrival. Supports sequential multi-waypoint missions.

### Camera Feed — `camera_feed.py`
Captures and displays live camera stream from onboard camera. Saves frames on demand. Foundation for onboard vision processing pipeline.

### Obstacle Detection — `obstacle_detection.py`
Applies OpenCV Canny edge detection to the live camera feed to identify obstacles in the flight path. Designed as a lightweight, real-time module suitable for embedded hardware.

### Object Tracking — `object_tracking.py`
MOSSE tracker for real-time target selection and lock-on. Operator selects target ROI; tracker maintains lock across frames. Foundation for intercept, follow-me, or target-designation applications.

### Return to Launch — `return_to_launch.py`
Triggers RTL mode and monitors descent to safe auto-land. Disarms vehicle and closes MAVLink connection cleanly after touchdown.

---

## Quick Start

### Install dependencies

```bash
pip install dronekit opencv-python numpy pymavlink
pip install dronekit-sitl  # for simulation only
```

### Run in SITL simulation

```bash
# Terminal 1 — start simulated ArduCopter
dronekit-sitl copter --home=48.1351,11.5820,520,0  # Munich coordinates

# Terminal 2 — run connection test
python connection.py
```

### Deploy on real hardware

```python
# USB / telemetry radio
vehicle = connect('/dev/ttyUSB0', baud=57600, wait_ready=True)

# UDP (companion computer / network link)
vehicle = connect('udp:192.168.1.1:14550', wait_ready=True)
```

---

## Relevant Applications

This control stack is directly applicable to:

- **Autonomous interception missions** — GPS-guided approach, target tracking, RTL
- **Counter-UAS systems** — perception pipeline for detecting and tracking airborne targets
- **Payload delivery / inspection UAVs** — waypoint nav + camera + safe return
- **Search and track** — MOSSE tracker adapted for airborne target lock

---

## Background

**B.Tech. Mechanical Engineering** — Rajasthan Technical University (2012–2016)
Final year project: Design, structural analysis, and test flight of a Quadcopter UAV and compressed-air vehicle (CRAVE). Covered aerodynamic modelling, frame stress analysis, motor and ESC selection, and manual/autonomous flight testing.

**M.Sc. Energy Engineering** — Technische Universität Berlin (2018–2021)
Thesis: *Custom Battery Cell Balancing Circuit Design Under Thermal Gradient* — thermal simulation framework (CFD/HyperWorks), MATLAB-Simulink lifetime analysis. Relevant to battery-powered UAV endurance and thermal management.

---

## Roadmap

- [ ] YOLO-based object detection for improved target classification
- [ ] Geofencing with automatic boundary enforcement
- [ ] ArduPilot Mission Planner integration for complex mission upload
- [ ] ROS2 integration for sensor fusion and advanced autonomy
- [ ] Multi-drone coordination basics

---

## Author

**Prateek Gaur** — Munich, Germany

M.Sc. Energy Engineering · TU Berlin | B.Tech. Mechanical Engineering · RTU

Applied ML Engineer with background in UAV design, battery systems, and autonomous system development.

[Portfolio](https://prateek-gaur-ml-bz0s69q.gamma.site/) | [LinkedIn](https://www.linkedin.com/in/prateek-gaur-15a629b4) | [GitHub](https://github.com/PRATdoppelEK)
