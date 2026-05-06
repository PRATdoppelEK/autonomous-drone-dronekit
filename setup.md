# Setup Guide

## Simulation Setup (Recommended for Testing)

### Step 1: Install Dependencies

```bash
pip install dronekit dronekit-sitl opencv-python numpy pymavlink
```

### Step 2: Start SITL Simulation

```bash
# Install dronekit-sitl if not already installed
pip install dronekit-sitl

# Start a simulated copter at a specific GPS location
dronekit-sitl copter --home=47.397742,8.545594,584,353
```

This starts a simulated ArduCopter at the given coordinates (lat, lon, altitude, heading).

### Step 3: Run a Script

Open a new terminal and run any script:

```bash
python connection.py
python arm_takeoff.py
python navigation.py
python examples/full_mission.py
```

---

## Real Hardware Setup

### Connection Options

| Method | Connection String | Notes |
|--------|-----------------|-------|
| USB/Serial | `/dev/ttyUSB0` | Linux; use `COM3` on Windows |
| UDP | `udp:192.168.1.1:14550` | Telemetry radio or WiFi |
| TCP | `tcp:192.168.1.1:5760` | Mission Planner companion |

### Example

```python
from dronekit import connect

# Serial connection (telemetry radio)
vehicle = connect('/dev/ttyUSB0', baud=57600, wait_ready=True)

# UDP connection
vehicle = connect('udp:192.168.1.1:14550', wait_ready=True)
```

### Camera Stream (Real Drone)

Replace `cv2.VideoCapture(0)` in camera scripts with your drone's stream URL:

```python
# RTSP stream (common on many FPV systems)
cap = cv2.VideoCapture('rtsp://192.168.1.1:554/stream')

# UDP stream
cap = cv2.VideoCapture('udp://127.0.0.1:5600')
```

---

## Tested Environment

- Python 3.8+
- Ubuntu 20.04 / 22.04
- DroneKit 2.9.2
- OpenCV 4.5+
- ArduCopter SITL via dronekit-sitl

---

## Common Issues

**"Waiting for vehicle to initialise" loops forever**
→ GPS fix takes time in SITL. Wait 30–60 seconds or check SITL output for errors.

**OpenCV tracker not found**
→ Install the contrib package: `pip install opencv-contrib-python`

**Connection refused on 127.0.0.1:14550**
→ Make sure SITL is running in a separate terminal before launching scripts.
