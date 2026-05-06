"""
navigation.py
-------------
GPS-based waypoint navigation using DroneKit's simple_goto.
Fly to one or more GPS coordinates at a specified altitude.

Usage:
    python navigation.py
"""

from dronekit import connect, VehicleMode, LocationGlobalRelative
from arm_takeoff import arm_and_takeoff
import time
import math


def get_distance_metres(location1, location2):
    """
    Approximate distance (in metres) between two LocationGlobal objects.
    Uses Haversine approximation — accurate for short distances.

    Args:
        location1: LocationGlobal or LocationGlobalRelative
        location2: LocationGlobal or LocationGlobalRelative

    Returns:
        float: Distance in metres.
    """
    dlat = location2.lat - location1.lat
    dlon = location2.lon - location1.lon
    return math.sqrt((dlat * dlat) + (dlon * dlon)) * 1.113195e5


def goto_waypoint(vehicle, lat, lon, alt, groundspeed=5, arrival_threshold=1.0):
    """
    Fly to a specific GPS waypoint.

    Args:
        vehicle: DroneKit vehicle object.
        lat (float): Target latitude.
        lon (float): Target longitude.
        alt (float): Target altitude in metres (relative).
        groundspeed (float): Flight speed in m/s.
        arrival_threshold (float): Distance in metres to consider waypoint reached.
    """
    target = LocationGlobalRelative(lat, lon, alt)
    print(f"Flying to: lat={lat}, lon={lon}, alt={alt}m at {groundspeed}m/s")

    vehicle.groundspeed = groundspeed
    vehicle.simple_goto(target)

    # Wait until close to the target
    while True:
        current = vehicle.location.global_relative_frame
        distance = get_distance_metres(current, target)
        print(f"  Distance to waypoint: {distance:.2f}m | Altitude: {current.alt:.2f}m")

        if distance < arrival_threshold:
            print(f"  Waypoint reached (within {arrival_threshold}m).")
            break

        time.sleep(1)


def fly_mission(vehicle, waypoints, cruise_altitude=20, groundspeed=5):
    """
    Execute a multi-waypoint mission.

    Args:
        vehicle: DroneKit vehicle object.
        waypoints (list): List of (lat, lon) tuples.
        cruise_altitude (float): Altitude in metres for all waypoints.
        groundspeed (float): Speed in m/s.
    """
    print(f"\nStarting mission with {len(waypoints)} waypoints at {cruise_altitude}m altitude.")

    for i, (lat, lon) in enumerate(waypoints):
        print(f"\n--- Waypoint {i+1}/{len(waypoints)} ---")
        goto_waypoint(vehicle, lat, lon, cruise_altitude, groundspeed)
        time.sleep(2)  # Brief hover at each waypoint

    print("\nMission complete. Returning to launch...")


if __name__ == "__main__":
    vehicle = connect('127.0.0.1:14550', wait_ready=True)

    try:
        # Take off to 15 metres
        arm_and_takeoff(vehicle, target_altitude=15)

        # Define waypoints (lat, lon) — example coordinates near Zurich
        waypoints = [
            (47.397742, 8.545594),
            (47.398242, 8.545994),
            (47.397842, 8.546594),
        ]

        fly_mission(vehicle, waypoints, cruise_altitude=15, groundspeed=5)

    finally:
        print("Initiating RTL...")
        vehicle.mode = VehicleMode("RTL")
        time.sleep(10)
        vehicle.close()
        print("Disconnected.")
