# Python Radar GUI

This folder contains the Python GUI software for the Arduino Ultrasonic Radar System.

## Files
- `radar_gui.py` — Python GUI source code.
- `requirements.txt` — Python dependency list.

## Requirements
- Python 3
- Arduino Uno
- HC-SR04 ultrasonic sensor
- Servo motor

## Installation
Install the required Python library:

```bash
pip install -r requirements.txt
```

## How to Run
1. Connect the Arduino to your computer using USB.
2. Upload the Arduino program from the `hardware` folder.
3. Check the Arduino's COM port and update the port setting in `radar_gui.py` if needed.
4. Run:

```bash
python radar_gui.py
```

**Note:** The Arduino COM port and baud rate in the Python code must match the Arduino setup.
