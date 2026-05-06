"""
connection.py
-------------
Connect to a drone via MAVLink and read basic telemetry data.
Works with both SITL simulation and real hardware.

Usage:
    python connection.py
"""

from dronekit import connect, VehicleMode
import time


def connect_drone(connection_string='127.0.0.1:14550', baud=None):
    """
    Connect to the vehicle and return the vehicle object.

    Args:
        connection_string (str): MAVLink connection string.
                                 Simulation:  '127.0.0.1:14550'
                                 USB serial:  '/dev/ttyUSB0'
                                 UDP:         'udp:192.168.1.1:14550'
        baud (int): Baud rate for serial connections (e.g. 57600).

    Returns:
        vehicle: DroneKit vehicle object.
    """
    print(f"Connecting to drone on: {connection_string}")

    if baud:
        vehicle = connect(connection_string, baud=baud, wait_ready=True)
    else:
        vehicle = connect(connection_string, wait_ready=True)

    print("Drone connected successfully.\n")
    return vehicle


def print_telemetry(vehicle):
    """Print key telemetry data from the vehicle."""
    print("--- Telemetry Data ---")
    print(f"GPS:          {vehicle.gps_0}")
    print(f"Battery:      {vehicle.battery}")
    print(f"Flight Mode:  {vehicle.mode.name}")
    print(f"Armed:        {vehicle.armed}")
    print(f"Altitude:     {vehicle.location.global_relative_frame.alt:.2f} m")
    print(f"Heading:      {vehicle.heading}°")
    print(f"Groundspeed:  {vehicle.groundspeed:.2f} m/s")
    print(f"System status:{vehicle.system_status.state}")
    print("----------------------\n")


if __name__ == "__main__":
    vehicle = connect_drone()
    print_telemetry(vehicle)

    # Monitor telemetry for 10 seconds
    print("Monitoring telemetry for 10 seconds...")
    for i in range(10):
        print(f"Altitude: {vehicle.location.global_relative_frame.alt:.2f} m | "
              f"Battery: {vehicle.battery.voltage:.2f}V | "
              f"Mode: {vehicle.mode.name}")
        time.sleep(1)

    vehicle.close()
    print("Disconnected.")
