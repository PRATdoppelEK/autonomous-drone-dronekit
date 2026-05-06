"""
examples/full_mission.py
------------------------
Complete autonomous mission example combining:
- Connection and telemetry
- Arm and takeoff
- Multi-waypoint navigation
- Return to launch

Run this for a full end-to-end simulation test.

Usage:
    python examples/full_mission.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dronekit import connect, VehicleMode
from arm_takeoff import arm_and_takeoff
from navigation import fly_mission
from return_to_launch import return_to_launch
from connection import print_telemetry
import time


def run_full_mission():
    """Execute a complete autonomous mission."""

    print("=" * 50)
    print("  Autonomous Drone Mission – Full Test")
    print("=" * 50)

    # Connect
    print("\n[1/4] Connecting to drone...")
    vehicle = connect('127.0.0.1:14550', wait_ready=True)
    print_telemetry(vehicle)

    try:
        # Takeoff
        print("\n[2/4] Arm and takeoff...")
        arm_and_takeoff(vehicle, target_altitude=15)
        print("Hovering for 3 seconds...")
        time.sleep(3)

        # Navigate waypoints
        print("\n[3/4] Starting waypoint navigation...")
        waypoints = [
            (47.397742, 8.545594),
            (47.398242, 8.545994),
            (47.397842, 8.546594),
            (47.397442, 8.545994),
        ]
        fly_mission(vehicle, waypoints, cruise_altitude=15, groundspeed=5)

        # Return to launch
        print("\n[4/4] Returning to launch...")
        return_to_launch(vehicle, wait_for_landing=True)

        print("\n" + "=" * 50)
        print("  Mission completed successfully.")
        print("=" * 50)

    except Exception as e:
        print(f"\nMission error: {e}")
        print("Attempting emergency RTL...")
        vehicle.mode = VehicleMode("RTL")
        time.sleep(10)

    finally:
        vehicle.close()
        print("Disconnected.")


if __name__ == "__main__":
    run_full_mission()
