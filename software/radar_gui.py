import tkinter as tk
import math
import serial
import serial.tools.list_ports

# ---------- SETTINGS ----------
PORT = "COM17"       # Change this to your Arduino port
BAUD_RATE = 9600
MAX_DISTANCE = 40    # Radar display range in cm

BG = "#020b05"
GREEN = "#62f51f"
RED = "#ff2020"
DIM_GREEN = "#1c6b29"
WHITE = "#d8ffd8"

# ---------- SERIAL CONNECTION ----------
ser = None

try:
    ser = serial.Serial(PORT, BAUD_RATE, timeout=0.01)
    ser.reset_input_buffer()
except serial.SerialException as e:
    print("Serial connection failed:", e)
    print("Available ports:")
    for p in serial.tools.list_ports.comports():
        print(" ", p.device, "-", p.description)

# ---------- GUI ----------
root = tk.Tk()
root.title("ELECTRICAL MANDIR - ARDUINO RADAR")
root.configure(bg=BG)
root.geometry("1100x760")
root.minsize(800, 600)

canvas = tk.Canvas(
    root, bg=BG, highlightthickness=0
)
canvas.pack(fill="both", expand=True)

current_angle = 90
current_distance = 0
object_points = []
last_data = ""
status = "CONNECTING" if ser else "DISCONNECTED"


def draw_radar():
    canvas.delete("all")

    w = canvas.winfo_width()
    h = canvas.winfo_height()

    # Keep a semicircular radar that fits the window.
    radius = min(w * 0.43, h * 0.68)
    ox = w / 2
    oy = h - 95

    if radius < 50:
        return

    def point(angle, r):
        rad = math.radians(angle)
        return ox + r * math.cos(rad), oy - r * math.sin(rad)

    # Distance rings
    for cm in (10, 20, 30, 40):
        r = radius * cm / MAX_DISTANCE
        coords = []

        for a in range(0, 181, 2):
            x, y = point(a, r)
            coords.extend((x, y))

        canvas.create_line(
            *coords, fill=GREEN, width=1
        )

        x, y = point(145, r)
        canvas.create_text(
            x, y - 12, text=f"{cm} cm",
            fill=GREEN, font=("Consolas", 10)
        )

    # Angle lines and labels
    for angle in range(0, 181, 30):
        x, y = point(angle, radius)
        canvas.create_line(
            ox, oy, x, y, fill=DIM_GREEN, width=1
        )

        lx, ly = point(angle, radius + 22)
        canvas.create_text(
            lx, ly, text=str(angle),
            fill=GREEN, font=("Consolas", 10)
        )

    # Baseline
    canvas.create_line(
        ox - radius, oy, ox + radius, oy,
        fill=GREEN, width=2
    )

    # Previously detected objects
    for angle, dist in object_points:
        if 0 < dist <= MAX_DISTANCE:
            r = radius * dist / MAX_DISTANCE
            x, y = point(angle, r)
            canvas.create_oval(
                x - 4, y - 4, x + 4, y + 4,
                fill=RED, outline=RED
            )

    # Current scanning line
    x, y = point(current_angle, radius)
    canvas.create_line(
        ox, oy, x, y, fill=GREEN, width=3
    )

    # Current distance readout
    if 0 < current_distance <= MAX_DISTANCE:
        r = radius * current_distance / MAX_DISTANCE
        x, y = point(current_angle, r)
        canvas.create_oval(
            x - 6, y - 6, x + 6, y + 6,
            fill=RED, outline=WHITE, width=1
        )

    # Bottom information panel
    panel_y = h - 65
    canvas.create_text(
        18, panel_y, anchor="w",
        text="ELECTRICAL MANDIR",
        fill=GREEN, font=("Consolas", 18, "bold")
    )

    canvas.create_text(
        w * 0.43, panel_y, anchor="w",
        text=f"ANGLE: {current_angle} deg",
        fill=GREEN, font=("Consolas", 14)
    )

    dist_text = (
        f"{current_distance} cm"
        if current_distance > 0
        else "NO ECHO"
    )
    canvas.create_text(
        w * 0.68, panel_y, anchor="w",
        text=f"DISTANCE: {dist_text}",
        fill=GREEN, font=("Consolas", 14)
    )

    canvas.create_text(
        w - 18, 18, anchor="ne",
        text=f"SERIAL: {status}",
        fill=GREEN if ser else RED,
        font=("Consolas", 11)
    )


def read_serial():
    global current_angle, current_distance
    global last_data, status, object_points

    if ser is not None:
        try:
            # Read incoming bytes without blocking the GUI.
            waiting = ser.in_waiting
            if waiting:
                chunk = ser.read(waiting).decode(
                    "ascii", errors="ignore"
                )
                last_data += chunk

                # Arduino sends angle,distance.\n
                while "." in last_data:
                    packet, last_data = last_data.split(".", 1)
                    packet = packet.strip()

                    if "," not in packet:
                        continue

                    try:
                        a, d = packet.split(",", 1)
                        angle = int(a)
                        dist = int(d)

                        if not 0 <= angle <= 180:
                            continue
                        if not 0 <= dist <= 500:
                            continue

                        current_angle = angle
                        current_distance = dist

                        if 0 < dist <= MAX_DISTANCE:
                            object_points.append((angle, dist))
                            # Limit memory and old marks
                            object_points = object_points[-250:]

                        status = "CONNECTED"

                    except ValueError:
                        continue

        except (serial.SerialException, OSError) as e:
            status = "SERIAL ERROR"
            print("Serial read error:", e)

    draw_radar()
    root.after(30, read_serial)


def clear_objects():
    global object_points
    object_points = []
    draw_radar()


def close_app():
    if ser is not None and ser.is_open:
        ser.close()
    root.destroy()


clear_button = tk.Button(
    root, text="CLEAR OBJECTS",
    command=clear_objects,
    bg="#12351a", fg=GREEN,
    activebackground="#20552b",
    activeforeground="white",
    font=("Consolas", 10)
)
clear_button.place(relx=0.5, rely=1.0, anchor="s", y=-5)

root.protocol("WM_DELETE_WINDOW", close_app)
root.after(200, read_serial)
root.mainloop()