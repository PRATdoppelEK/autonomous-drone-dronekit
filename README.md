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
