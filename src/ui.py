import tkinter as tk
import tkinter.font as tkfont
from app_manager import temp_to_color, TEMP_MAX, TEMP_CIRCLE_RAD


class RoundedButton(tk.Canvas):
    def __init__(self, parent, cfg, command):
        self._color = cfg.color
        self._color_active = cfg.color_active
        self._command = command

        super().__init__(
            parent,
            width=cfg.width,
            height=cfg.height,
            bg=parent["bg"],
            highlightthickness=0,
        )

        points = self._make_points(2, 2, cfg.width - 4, cfg.height - 4, cfg.radius)
        self._rect = self.create_polygon(points, smooth=True, fill=cfg.color, outline="")
        self._label = self.create_text(
            cfg.width // 2,
            cfg.height // 2,
            text=cfg.text,
            fill=cfg.text_color,
            font=(cfg.font_family, cfg.font_size),
        )

        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    @staticmethod
    def _make_points(x, y, w, h, r):
        return [
            x + r, y, x + w - r, y, x + w, y, x + w, y + r,
            x + w, y + h - r, x + w, y + h, x + w - r, y + h,
            x + r, y + h, x, y + h, x, y + h - r, x, y + r, x, y,
        ]

    def _on_press(self, _):
        self.itemconfig(self._rect, fill=self._color_active)

    def _on_release(self, _):
        self.itemconfig(self._rect, fill=self._color)
        self._command()


class Window:
    def __init__(self, width, height, root, data, cfg):
        self.root = root
        self.data = data
        self.font = tkfont.Font(family="Cascadia Mono", size=28)
        self.canvas = tk.Canvas(self.root, bg="#2E2E2E", height=height, width=width)

        self.root.title("Czujniki w pokoju")
        self.root.geometry(f"{width}x{height}")

        self.screen = tk.Frame(self.root, padx=20, pady=20, bg="#2E2E2E")
        self.screen.pack(expand=False, fill="both")

        self.canvas.create_text(200, 60, text="Temperatura:", font=self.font, fill="#FFFFFF")
        self.canvas.pack()

    def draw_animation(self, center, rad: float, data: float):
        cx, cy = center
        start = 90
        max_angle = 330
        arc_length = (max_angle - start) / 100
        simulated_temp = 0

        for i in range(int(data / TEMP_MAX * 100)):
            self.canvas.create_arc(
                cx - rad, cy - rad, cx + rad, cy + rad,
                start=start + arc_length * i,
                extent=arc_length + 1,
                style=tk.ARC,
                width=15,
                outline=temp_to_color(simulated_temp),
                tags="circle_animation",
            )
            simulated_temp = i * (TEMP_MAX / 100)

        self.canvas.create_oval(
            cx - TEMP_CIRCLE_RAD, cy - TEMP_CIRCLE_RAD,
            cx + TEMP_CIRCLE_RAD, cy + TEMP_CIRCLE_RAD,
            fill="#383838", tags="circle",
        )
        self.canvas.create_text(cx, cy, font=self.font, text=f"{data:.1f}°C", fill="#FFFFFF", tags="txt")

    def bar_animation(self, start, end, width, label: str, data: float, min_value, max_value):
        sx, sy = start
        ex, ey = end

        t = (data - min_value) / (max_value - min_value)
        progress = tuple(s + (e - s) * t for s, e in zip(start, end))
        px, py = progress

        self.canvas.create_oval(ex - width, ey - width, ex + width, ey + width, fill="#666666", tags="bar")
        txt_x, txt_y = (sx + ex) / 2, (sy + ey) / 2 - 50
        self.canvas.create_text(txt_x, txt_y, fill="#FFFFFF", tags="bar", text=label, font=(self.font, 24))
        self.canvas.create_oval(sx - width, sy - width, sx + width, sy + width, fill="#519FC9", tags="bar")
        self.canvas.create_line(sx, sy, ex, ey, width=width * 2, fill="#666666", tags="bar")
        self.canvas.create_oval(px - width, py - width, px + width, py + width, fill="#519FC9", tags="bar")
        self.canvas.create_line(sx, sy, px, py, width=width * 2, fill="#519FC9", tags="bar")
