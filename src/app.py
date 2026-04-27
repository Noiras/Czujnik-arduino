import tkinter as tk
import tkinter.font as tkfont
import threading  # odpowiednik java.lang.Thread
import queue  # thread-safe kolejka do przekazywania danych między wątkami (jak BlockingQueue w Javie)
import serial
import data
import os
from config import load_config

config = load_config()

# stałe konfiguracyjne w jednym miejscu — zmiana portu/baud rate tylko tutaj
COM_PORT = config.com_port
BAUD_RATE = config.baud_rate
DB_PATH = config.db_path
TEMP_MAX = 40.0
TEMP_CIRCLE_RAD = 70

data.initalize(DB_PATH)
con = data.get_con(DB_PATH)


# model danych oddzielony od widoku — przechowuje aktualne wartości sensorów
# domyślne wartości działają jako placeholder zanim nadejdą dane z Arduino
class SensorData:
    def __init__(self):
        self.temp = 33.0
        self.humidity = 40.0
        self.pressure = 1020.0


class Window:
    def __init__(self, width, height, root, data):
        self.root = root
        self.data = (
            data  # referencja do SensorData — widok czyta dane stąd, nie z globals
        )
        self.canvas = tk.Canvas(self.root, bg="#2E2E2E", height=height, width=width)

        self.root.title("Czujniki w pokoju")
        self.root.geometry(
            f"{width}x{height}"
        )  # kolejność: width x height (poprzednio było odwrotnie)

        self.screen = tk.Frame(self.root, padx=20, pady=20)
        self.screen.pack(expand=False, fill="both")

        self.canvas.create_text(200, 60, text="Temperatura:", font=font, fill="#FFFFFF")
        self.canvas.pack()

    def draw_animation(self, center, rad: float, data: float):
        cx, cy = center
        start = 90
        max_angle = 330

        arc_length = (max_angle - start) / 100
        simulated_temp = 0

        for i in range(int(data / TEMP_MAX * 100)):
            self.canvas.create_arc(
                cx - rad,
                cy - rad,
                cx + rad,
                cy + rad,
                start=start + arc_length * i,
                extent=arc_length + 1,
                style=tk.ARC,
                width=15,
                outline=temp_to_color(simulated_temp),
                tags="circle_animation",
            )
            simulated_temp = i * (TEMP_MAX / 100)

        self.canvas.create_oval(
            cx - TEMP_CIRCLE_RAD,
            cy - TEMP_CIRCLE_RAD,
            cx + TEMP_CIRCLE_RAD,
            cy + TEMP_CIRCLE_RAD,
            fill="#383838",
            tags="circle",
        )
        self.canvas.create_text(
            cx,
            cy,
            font=font,
            text=f"{data:.1f}°C",
            fill="#FFFFFF",
            tags="txt",
        )

    def bar_animation(
        self, start, end, width, label: str, data: float, min_value, max_value
    ):
        sx, sy = start
        ex, ey = end

        t = (data - min_value) / (max_value - min_value)

        progress = tuple(s + (e - s) * t for s, e in zip(start, end))
        px, py = progress

        self.canvas.create_oval(
            ex - width, ey - width, ex + width, ey + width, fill="#666666", tags="bar"
        )
        txt_x, txt_y = (sx + ex) / 2, (sy + ey) / 2 - 50
        self.canvas.create_text(
            txt_x,
            txt_y,
            fill="#FFFFFF",
            tags="bar",
            text=label,
            font=(font, 24),
        )
        self.canvas.create_oval(
            sx - width, sy - width, sx + width, sy + width, fill="#519FC9", tags="bar"
        )
        self.canvas.create_line(
            sx, sy, ex, ey, width=width * 2, fill="#666666", tags="bar"
        )
        self.canvas.create_oval(
            px - width,
            py - width,
            px + width,
            py + width,
            fill="#519FC9",
            tags="bar",
        )
        self.canvas.create_line(
            sx, sy, px, py, width=width * 2, fill="#519FC9", tags="bar"
        )


def rgb_to_hex(r, g, b):
    return "#" + ("{:02X}" * 3).format(r, g, b)


def temp_to_color(temp: float) -> str:
    t = max(0.0, min(1.0, temp / TEMP_MAX))  # clamp do [0, 1]
    r = int(122 + (230 - 122) * t)  # 122 → 230 (rośnie R)
    g = int(230 + (14 - 230) * t)  # 230 → 14  (maleje G)
    b = 14  # B stały
    return rgb_to_hex(r, g, b)


# działa w osobnym wątku — blokujący readline() nie zatrzymuje GUI
# dane wrzucane do serial_queue, skąd odbiera je update() w wątku głównym
def serial_reader(data_queue):
    try:
        s = serial.Serial(COM_PORT, BAUD_RATE)
        while True:
            line = s.readline().decode("utf-8").split(",")
            data_queue.put(line)
            data.put_data(con, line)
    except Exception as e:
        print(f"Błąd seriala: {e}")

    # TODO: dodać obsługę UnicodeDecodeError osobno (uszkodzone bajty z Arduino)
    # TODO: dodać logikę ponownego połączenia po utracie portu (np. Arduino reset)


def parse_line(line, sensor_data):
    # oczekiwany format z Arduino: "temp,humidity,pressure"
    try:
        parts = line.split(",")
        sensor_data.temp = float(parts[0])
        sensor_data.humidity = float(parts[1])
        sensor_data.pressure = float(parts[2])
    except (ValueError, IndexError):
        pass  # TODO: logować błędne linie zamiast cicho je ignorować


sensor_data = SensorData()
serial_queue = (
    queue.Queue()
)  # thread-safe — serial_reader pisze, update() czyta bez race condition

root = tk.Tk()
# font musi być stworzony po tk.Tk() — tkinter wymaga aktywnego root przed tworzeniem fontów
font = tkfont.Font(family="Cascadia Mono", size=28)
w = Window(800, 800, root=root, data=sensor_data)


def update():
    # opróżnia kolejkę ze wszystkich linii które nadeszły od ostatniej klatki
    # TODO: bardziej idiomatycznie: try/except queue.Empty zamiast empty() + get_nowait()
    # empty() + get_nowait() to TOCTOU — poprawna wersja: while True: try: get_nowait() except Empty: break
    while not serial_queue.empty():
        parse_line(serial_queue.get_nowait(), sensor_data)

    w.canvas.delete(
        "line", "circle", "txt", "txt2", "circle_animation", "bar"
    )  # czyści tylko tagowane elementy, nie cały canvas
    w.bar_animation(
        (500, 150),
        (700, 150),
        10,
        f"Wilgotność: {sensor_data.humidity:.0f}%",
        data=sensor_data.humidity,
        min_value=0,
        max_value=100,
    )
    w.bar_animation(
        (500, 350),
        (700, 350),
        10,
        f"Ciśnienie: {sensor_data.pressure:.0f}hPa",
        data=sensor_data.pressure,
        min_value=950,
        max_value=1050,
    )
    w.draw_animation((200, 250), TEMP_CIRCLE_RAD + 10, sensor_data.temp)
    root.after(
        10, update
    )  # zamiast while+sleep — planuje następne wywołanie za 10ms przez event loop


# daemon=True — wątek kończy się automatycznie gdy zamkniesz okno (jak setDaemon(true) w Javie)
threading.Thread(target=serial_reader, args=(serial_queue,), daemon=True).start()
root.after(10, update)
root.mainloop()  # przekazuje kontrolę do event loop tkinter — odpowiednik SwingUtilities w Javie
