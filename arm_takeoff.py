"""
arm_takeoff.py
--------------
Arm the vehicle and execute a controlled takeoff sequence.
Includes safety checks before arming.

Usage:
    python arm_takeoff.py
"""

from dronekit import connect, VehicleMode
import time


def arm_and_takeoff(vehicle, target_altitude):
    """
    Perform pre-arm checks, arm the vehicle, and take off to target altitude.

    Args:
        vehicle: DroneKit vehicle object.
        target_altitude (float): Target altitude in metres (relative to launch point).
    """
    print("Running pre-arm checks...")

    # Wait until the vehicle is armable
    while not vehicle.is_armable:
        print("  Waiting for vehicle to initialise (GPS fix, EKF ready)...")
        time.sleep(1)

    print("Vehicle is armable. Setting GUIDED mode...")
    vehicle.mode = VehicleMode("GUIDED")

    # Wait until mode is confirmed
    while vehicle.mode.name != "GUIDED":
        print("  Waiting for GUIDED mode...")
        time.sleep(1)

    print("Arming motors...")
    vehicle.armed = True

    # Wait until armed
    while not vehicle.armed:
        print("  Waiting for arming...")
        time.sleep(1)

    print(f"Armed. Taking off to {target_altitude}m...")
    vehicle.simple_takeoff(target_altitude)

    # Monitor altitude until target is reached
    while True:
        current_alt = vehicle.location.global_relative_frame.alt
        print(f"  Altitude: {current_alt:.2f}m")

        # Reached 95% of target altitude — close enough
        if current_alt >= target_altitude * 0.95:
            print(f"Target altitude of {target_altitude}m reached.")
            break

        time.sleep(1)


if __name__ == "__main__":
    vehicle = connect('127.0.0.1:14550', wait_ready=True)

    try:
        arm_and_takeoff(vehicle, target_altitude=10)
        print("Hovering for 5 seconds...")
        time.sleep(5)
    finally:
        print("Landing...")
        vehicle.mode = VehicleMode("LAND")
        time.sleep(5)
        vehicle.close()
        print("Done.")
