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
