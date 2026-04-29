# Notatki — Czujnik Arduino

## Sesja 2026-04-25 — animacje tkinter canvas

### `canvas.create_arc`

```python
canvas.create_arc(x0, y0, x1, y1, start=..., extent=..., style=..., width=..., outline=...)
```

- `x0, y0, x1, y1` — bounding box **pełnej elipsy**, nie punkty łuku
- `start` i `extent` w **stopniach** (nie radianach) — częsty błąd
- `extent` to **rozmiar kąta** segmentu, nie kąt końcowy
- `style=tk.ARC` — sama linia łuku (bez wypełnienia do środka)
- `style=tk.PIESLICE` — łuk + linie do środka (jak kawałek tortu)

### Gradient przez wiele segmentów arc

- Dzielisz łuk na N małych segmentów, każdy z osobnym kolorem wyliczonym przez lerp
- `extent = arc_length + 1` — mały overlap eliminuje wcięcia między segmentami
- `canvas.delete(tag)` **przed** rysowaniem — bez tego segmenty akumulują się każdą klatką

### Lerp koloru (green → red)

```python
def temp_to_color(temp: float) -> str:
    t = max(0.0, min(1.0, temp / TEMP_MAX))  # clamp do [0, 1]
    r = int(r_start + (r_end - r_start) * t)
    g = int(g_start + (g_end - g_start) * t)
    return rgb_to_hex(r, g, b)
```

### Normalizacja zakresu wartości (pasek postępu)

```python
t = (value - min_val) / (max_val - min_val)  # działa dla dowolnego zakresu (np. ciśnienie 950–1050)
progress = tuple(s + (e - s) * t for s, e in zip(start_point, end_point))
px, py = progress  # unpack przed użyciem w canvas
```

### Pułapki

| Problem | Rozwiązanie |
|---------|-------------|
| `range(N)` — start domyślnie `0` | `range(N)` == `range(0, N)` |
| `args=(x)` w `Thread` — to nie tuple | `args=(x,)` — przecinek obowiązkowy |
| Mieszanie `for i in range(...)` z ręcznym licznikiem | Używaj `i`, wyrzuć osobną zmienną |
| `simulated_temp` rośnie kwadratowo gdy `+=` z rosnącą wartością | Użyj przypisania: `simulated_temp = i * (TEMP_MAX / 100)` |

---

## Sesja 2026-04-28 — SQLite, Pydantic, config, RoundedButton

### Pydantic v2 — Optional bez domyślnej wartości

```python
# źle — Pydantic v2 nadal wymaga podania pola
temperatura: Optional[float]

# dobrze
temperatura: Optional[float] = None
wilgotnosc: Optional[int] = Field(default=None, ge=0, le=100)
```

### SQLite — typowe błędy składni

```python
# błędna składnia INSERT
"INSERT INTO dane (?, ?, ?) with data=?"

# poprawnie
"INSERT INTO dane (temperatura, cisnienie, wilgotnosc, data_pomiaru) VALUES (?, ?, ?, ?)"

# błędna składnia SELECT
"SELECT * FROM dane WITH data=?"

# poprawnie
"SELECT * FROM dane WHERE data_pomiaru=?"
```

### sqlite3.Row jako row_factory — `**dict(row)`

```python
db.row_factory = sqlite3.Row
rows = db.execute("SELECT * FROM dane WHERE data_pomiaru=?", (data,)).fetchall()
return [data_structs.StructUpdate(**dict(row)) for row in rows]
```

`sqlite3.Row` pozwala na `dict(row)` → słownik z nazwami kolumn jako kluczami.  
Bez tego `fetchall()` zwraca tuple — nie można ich rozpakować przez `**`.

### Config z zagnieżdżonym modelem Pydantic

```python
class ButtonConfig(BaseModel):
    color: str
    color_active: str
    ...

class Config(BaseModel):
    db_path: Path
    save_button: ButtonConfig   # zagnieżdżony model — Pydantic waliduje rekurencyjnie
```

JSON z zagnieżdżonym obiektem jest automatycznie parsowany do `ButtonConfig`.

### RoundedButton — zaokrąglony prostokąt na Canvas

`create_polygon(points, smooth=True)` — B-spline przez 12 punktów (po 3 na narożnik):
- dwa punkty wzdłuż krawędzi w odległości `r` od narożnika → definiują prostą część
- sam narożnik → punkt kontrolny B-spline, przyciąga krzywą ale jej nie dotyka

```python
@staticmethod
def _make_points(x, y, w, h, r):
    return [
        x+r, y,    x+w-r, y,
        x+w, y,    x+w, y+r,
        x+w, y+h-r, x+w, y+h,
        x+w-r, y+h, x+r, y+h,
        x, y+h,    x, y+h-r,
        x, y+r,    x, y,
    ]
```

Zmiana koloru przy kliknięciu — `itemconfig`:
```python
def _on_press(self, _):
    self._canvas.itemconfig(self._rect, fill=self._color_active)

def _on_release(self, _):
    self._canvas.itemconfig(self._rect, fill=self._color)
    self._command()
```

### Osadzanie widgetu w Canvas — `create_window`

```python
# parent RoundedButton musi być canvas (nie Frame) w którym go osadzasz
self.save_btn = RoundedButton(self.canvas, cfg.save_button, on_save)

# window= obowiązkowy jako keyword argument
self.canvas.create_window(400, 500, window=self.save_btn._canvas)
```

Pułapki `create_window`:
- widget musi być dzieckiem tego samego canvasa — inaczej `TclError`
- trzeci pozycyjny argument to `cnf` (dict opcji), nie widget — `window=` jest wymagane

---

## Sesja 2026-04-29 — tkinter widgets, dziedziczenie, refaktor struktury

### Każda kontrolka tkinter to widget

`tk.Frame`, `tk.Canvas`, `tk.Button`, `tk.Label` — wszystko dziedziczy z `tk.BaseWidget`.  
Można przekazać dowolny z nich jako `parent` do innego widgetu.

```python
w.screen  # tk.Frame — też widget, można go użyć jako parent
w.canvas  # tk.Canvas — też widget
```

Hierarchia w projekcie:
```
tk.Tk (root)
├── tk.Frame  (w.screen)  ← kontener
└── tk.Canvas (w.canvas)  ← płótno do rysowania
    └── RoundedButton     ← osadzony przez create_window
```

### Kiedy dziedziczyć po tk.Canvas, a kiedy po tk.Frame

| Base class | Kiedy używać |
|---|---|
| `tk.Canvas` | Widget **jest** płótnem — rysuje się sam na sobie. Brak sub-widgetów. |
| `tk.Frame` | Widget **zawiera** inne widgety (np. ikona + label + przycisk). |

`RoundedButton` jest jednym canvasem z narysowanym kształtem → dziedziczy po `tk.Canvas`.  
Dziedziczenie po `tk.Frame` + wewnętrzny `tk.Canvas` to zbędna warstwa bez korzyści.

```python
class RoundedButton(tk.Canvas):
    def __init__(self, parent, cfg, command):
        super().__init__(parent, width=cfg.width, height=cfg.height, ...)
        self._rect = self.create_polygon(...)   # self zamiast self._canvas
        self.bind("<ButtonPress-1>", ...)       # pack/place/grid odziedziczone
```

### Trzy metody layoutu — pack / grid / place

```python
widget.pack(side="bottom", pady=20)          # stackuje w linii
widget.grid(row=2, column=0, padx=10)        # siatka
widget.place(x=300, y=400)                   # absolutne koordynaty
widget.place(relx=0.5, rely=0.9, anchor="center")  # relatywne (0.0–1.0)
```

`anchor` — który punkt widgetu trafia na podane koordynaty:  
`"nw"` (lewy-górny, domyślny) | `"center"` | `"n"`, `"s"`, `"e"`, `"w"`, `"ne"`, `"se"`, `"sw"`

### Osadzanie widgetu na Canvas — create_window (poprawiony przykład)

```python
button = RoundedButton(w.canvas, cfg=config.save_button, command=save_to_db)
w.canvas.create_window(400, 700, window=button, anchor="center")
# x=400, y=700 to koordynaty na canvasie
# widget musi być dzieckiem tego canvasa (parent=w.canvas)
```

Używaj `create_window` gdy chcesz precyzyjnie pozycjonować widget **wewnątrz canvasa**  
— `pack/place` pozycjonuje względem parenta-kontenera (Frame/root), nie canvasa.

### Circular imports — rozwiązanie przez klasę AppManager

Problem: `main.py` importuje funkcje z `app_manager.py`, a funkcje potrzebują `sensor_data`/`con` z `main.py` → circular import.

Rozwiązanie: dependency injection przez klasę — zależności przekazane w konstruktorze:

```python
class AppManager:
    def __init__(self, sensor_data, con, window, config):
        self.sensor_data = sensor_data
        self.con = con
        ...

    def save_to_db(self):          # używa self.sensor_data — bez importu main.py
        ...

    def serial_reader(self, queue):
        ...
```

```python
# main.py
manager = AppManager(sensor_data, con, w, config)
threading.Thread(target=manager.serial_reader, args=(serial_queue,), daemon=True).start()
button = RoundedButton(..., command=manager.save_to_db)
```

`app_manager.py` nie importuje nic z `main.py` — zero circular imports.

### Dostęp do opcji widgetu — subscript i cget

```python
parent["bg"]          # subscript — działa dla Canvas i Frame
parent.cget("bg")     # metoda — bardziej jawna, równoważna
```

Obie formy zwracają aktualną wartość opcji konfiguracyjnej widgetu (np. kolor tła).
