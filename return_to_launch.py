"""
return_to_launch.py
-------------------
Safe Return-to-Launch (RTL) and autonomous landing procedures.
Includes manual landing override option.

Usage:
    python return_to_launch.py
"""

from dronekit import connect, VehicleMode
import time


def return_to_launch(vehicle, wait_for_landing=True):
    """
    Command the vehicle to return to its launch location and land.

    Args:
        vehicle: DroneKit vehicle object.
        wait_for_landing (bool): If True, wait until the vehicle has landed.
    """
    print("Initiating Return to Launch (RTL)...")
    vehicle.mode = VehicleMode("RTL")

    # Confirm mode change
    while vehicle.mode.name != "RTL":
        print("  Waiting for RTL mode confirmation...")
        time.sleep(1)

    print("RTL mode confirmed. Vehicle returning to launch point.")

    if wait_for_landing:
        print("Waiting for landing...")
        while vehicle.location.global_relative_frame.alt > 0.5:
            print(f"  Altitude: {vehicle.location.global_relative_frame.alt:.2f}m")
            time.sleep(1)
        print("Vehicle has landed.")


def manual_land(vehicle):
    """
    Initiate autonomous landing at current position.

    Args:
        vehicle: DroneKit vehicle object.
    """
    print("Initiating manual landing at current position...")
    vehicle.mode = VehicleMode("LAND")

    while vehicle.mode.name != "LAND":
        print("  Waiting for LAND mode confirmation...")
        time.sleep(1)

    print("LAND mode confirmed. Descending...")

    while vehicle.location.global_relative_frame.alt > 0.5:
        print(f"  Altitude: {vehicle.location.global_relative_frame.alt:.2f}m")
        time.sleep(1)

    print("Vehicle has landed.")


def emergency_stop(vehicle):
    """
    Disarm the vehicle immediately (emergency use only).
    WARNING: Only use this on the ground or in a true emergency.

    Args:
        vehicle: DroneKit vehicle object.
    """
    print("EMERGENCY STOP: Disarming vehicle immediately.")
    vehicle.armed = False
    print("Vehicle disarmed.")


if __name__ == "__main__":
    vehicle = connect('127.0.0.1:14550', wait_ready=True)

    try:
        print(f"Current altitude: {vehicle.location.global_relative_frame.alt:.2f}m")
        print(f"Current mode: {vehicle.mode.name}")

        # Execute RTL
        return_to_launch(vehicle, wait_for_landing=True)

    finally:
        vehicle.close()
        print("Vehicle connection closed.")
