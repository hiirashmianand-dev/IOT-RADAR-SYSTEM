Hardware files for the Arduino Ultrasonic Radar System.

Hardware Components — Arduino Radar System

📌 Overview

This folder contains the hardware-related files for our Arduino-Based Radar System, developed as part of our Internet of Things (IoT) Project-Based Learning (PBL).

The system uses an Arduino UNO, an HC-SR04 ultrasonic sensor, and a servo motor to detect nearby objects and measure their approximate distances at different angles.

🔧 Hardware Components

* Arduino UNO
* HC-SR04 Ultrasonic Sensor
* Servo Motor
* Breadboard
* Jumper Wires
* USB Cable

📂 Files Included

File	Description
Arduino-Ultrasonic-Radar.ino	Arduino source code for controlling the servo motor, measuring distances, and transmitting sensor readings.
circuit_diagram.jpeg	Circuit diagram of the radar system.
Radar_HardwareIMG.jpeg	Photograph of the actual hardware setup.

⚙️ Working Principle

1. The servo motor rotates the ultrasonic sensor across a specified angular range.
2. The HC-SR04 sensor measures the distance to nearby objects using ultrasonic waves.
3. The Arduino processes the sensor readings.
4. The angle and distance data are transmitted to a computer through serial communication.
5. The Python application displays the detected objects on a radar-style graphical interface.

🎓 Project Information

Project: Arduino-Based Radar System
Domain: Internet of Things (IoT)
Department: Computer Science and Engineering (CSE)
Institution: Bharati Vidyapeeth (Deemed to be University) College of Engineering, Pune

👥 Team Members

* Digvijay Chavan
* Rashmi Anand
* Rushikesh Rajput
* Ayush Bariar
