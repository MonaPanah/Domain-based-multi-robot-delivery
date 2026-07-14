# Domain-Based Communication and Swarm Optimization Framework for Delivery Multi-Robot Systems Using LoRa
Design and simulation of a domain-based communication architecture for autonomous multi-robot delivery systems.

## Overview

This project implements a multi-robot delivery swarm simulation using:

- OMNeT++ 6.0.3
- INET Framework
- FLoRa Framework
- Python-based swarm optimization

The system combines:
- LoRa communication
- Robot authentication
- Distributed task sharing
- Swarm-based optimization
- Connectivity preservation
- Collision avoidance
- Priority-driven task execution

Each robot executes only its own assigned tasks while maintaining swarm coordination.

---

# Main Files

| File | Description |
|---|---|
| `AuthClient.cc / AuthClient.h` | Robot communication, authentication, task sharing, swarm logic |
| `PacketForwarder.cc / PacketForwarder.h` | Gateway communication and forwarding |
| `Swarm_python.py` | Swarm optimization engine |
| `omnetpp.ini` | Simulation configuration |
| `*.ned` | Network topology files |

---

# Requirements

Install:

- OMNeT++ 6.0.3
- INET Framework
- FLoRa Framework
- Python 3.x
- NumPy

Install NumPy:

```bash
pip install numpy
```

---

# Running the Project

## 1. Import the Project

Import the project into the OMNeT++ IDE.

---

## 2. Configure Frameworks

Make sure:

- INET is linked correctly
- FLoRa is linked correctly
- Python executable path inside `AuthClient.cc` is valid

Example:

```cpp
"C:\\Users\\USERNAME\\AppData\\Local\\Microsoft\\WindowsApps\\python3.exe"
```

---

## 3. Build the Project

```bash
make MODE=release all
```

or use:

Project → Build Project

---

## 4. Run the Simulation

Run using:

```ini
omnetpp.ini
```

The simulation performs:

1. Robot authentication
2. HELLO communication exchange
3. Distributed task sharing
4. Swarm optimization
5. Coordinated task execution

---

# Optimization Workflow

1. Gateway assigns tasks to robots
2. Robots authenticate to the domain
3. Robots exchange local task tables
4. Full task propagation is achieved
5. Master robot triggers Python optimization
6. Optimized execution order is generated
7. Results are shared across all robots

---

# Features

- LoRa-based communication
- Distributed swarm coordination
- Priority-based task execution
- Connectivity-aware movement
- Collision avoidance
- Dynamic swarm visualization
- Python-integrated optimization

---

# Notes

- Only one robot triggers the Python optimizer
- All robots receive the same optimization results
- Task reassignment is disabled
- Lower numerical value means higher priority

---

# Author

Maryam(Mona) Ghaem Panah

