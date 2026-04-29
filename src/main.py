import tkinter as tk
import threading
import queue
import data
from config import load_config
from ui import Window, RoundedButton
from app_manager import AppManager, SensorData, TEMP_CIRCLE_RAD

config = load_config()
DB_PATH = config.db_path

data.initalize(DB_PATH)
con = data.get_con(DB_PATH)

serial_queue = queue.Queue()
sensor_data = SensorData()

root = tk.Tk()
w = Window(800, 800, root=root, data=sensor_data, cfg=config)
manager = AppManager(sensor_data=sensor_data, con=con, window=w, config=config)

button_input = RoundedButton(parent=w.canvas, cfg=config.save_button, command=manager.save_to_db)
button_output = RoundedButton(parent=w.canvas, cfg=config.output_button, command=manager.print_table)
w.canvas.create_window(300, 700, anchor="center", window=button_input)
w.canvas.create_window(530, 700, anchor="center", window=button_output)


def update():
    while not serial_queue.empty():
        manager.parse_line(serial_queue.get_nowait())

    w.canvas.delete("line", "circle", "txt", "txt2", "circle_animation", "bar")
    w.bar_animation(
        (500, 150), (700, 150), 10,
        f"Wilgotność: {sensor_data.humidity:.0f}%",
        data=sensor_data.humidity, min_value=0, max_value=100,
    )
    w.bar_animation(
        (500, 350), (700, 350), 10,
        f"Ciśnienie: {sensor_data.pressure:.0f}hPa",
        data=sensor_data.pressure, min_value=950, max_value=1050,
    )
    w.draw_animation((200, 250), TEMP_CIRCLE_RAD + 10, sensor_data.temp)
    root.after(10, update)


threading.Thread(target=manager.serial_reader, args=(serial_queue,), daemon=True).start()
root.after(10, update)
root.mainloop()
