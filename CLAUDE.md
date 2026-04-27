# CLAUDE.md — projekt Czujnik-arduino

Kontekst projektu dla Claude. Preferencje ogólne (język, styl, poziom wyjaśnień) są w globalnym `~/.claude/CLAUDE.md` — tutaj tylko to co specyficzne dla tego projektu.

---

## Cel projektu

Stacja pomiarowa parametrów otoczenia łącząca hardware z softwarem:

```
[DHT22 + BMP280] → [Arduino Uno / ATmega328P] → [Serial CSV] → [Python desktop] → [tkinter GUI + SQLite]
```

Dane: **temperatura** (float, °C), **ciśnienie** (float, hPa), **wilgotność** (int, 0–100%).

---

## Struktura plików

```
src/
├── main.cpp          # Arduino C++ — odczyt sensorów, wysyłanie przez Serial
├── app.py            # główna pętla GUI (tkinter), serial reader w osobnym wątku
├── data_structs.py   # modele Pydantic — Struct, StructUpdate
├── data.py           # operacje SQLite — initialize(), get_con(), put_data(), get_data()
└── config.py         # ładowanie config.json — klasa Config (Pydantic), load_config()
config.json           # ścieżki i parametry: db_path, com_port, baud_rate
```

---

## Architektura — kluczowe decyzje

### Serial
- Format danych z Arduino: CSV `temperatura,wilgotnosc,cisnienie\n`
- `serial_reader()` działa w osobnym `daemon thread` — blokujące `readline()` nie blokuje GUI
- Dane przechodzą przez `queue.Queue` (thread-safe) do `update()` w event loop tkinter

### Config
- `config.json` — jedno miejsce dla wszystkich parametrów runtime
- Import stylem `from config import load_config` (nie `import config`)
- Instancja `Config` tworzona raz przy starcie: `configuration = load_config()`

### SQLite
- Połączenie (`get_con`) zwraca plain `sqlite3.Connection` — żyje przez cały czas działania apki
- Schemat tabeli: `dane (temperatura REAL, cisnienie REAL, wilgotnosc INTEGER, data_pomiaru TEXT)`
- `data_pomiaru` przechowywany jako ISO string (`datetime.datetime.now().isoformat()`)
- Przy odczycie wierszy używać `sqlite3.Row` jako `row_factory` żeby możliwe było `**dict(row)`

### Modele Pydantic
- `Struct` — dane do zapisu (wszystkie pola wymagane)
- `StructUpdate` — dane do wyszukiwania (temperatura/cisnienie/wilgotnosc opcjonalne + wymagane `data_pomiaru: str`)
- `Optional[X]` zawsze z `= None`, `Field` z `default=None` gdy Optional

---

## Stan Arduino (main.cpp)

Szkielet — do zaimplementowania:
- `Serial.begin(9600)` w `setup()`
- Inicjalizacja DHT22 i BMP280 w `setup()`
- Odczyt i wysyłka CSV w `loop()` z kontrolą częstotliwości przez `millis()` (nie `delay()`)

Biblioteki: `DHT` (temperatura + wilgotność), `Adafruit_BMP280` (ciśnienie).
Ograniczenia Uno: 2 KB SRAM, 32 KB flash — bez dynamicznych alokacji, bez String w pętli.

---

## Znane TODO w kodzie

- `serial_reader()`: brak obsługi `UnicodeDecodeError` i logiki reconnect po resecie Arduino
- `parse_line()`: błędne linie są cicho ignorowane — warto logować
- `update()` w app.py: wzorzec `empty() + get_nowait()` to TOCTOU — poprawnie: `try/except queue.Empty`
- `initalize()` w data.py: literówka w nazwie funkcji (brakuje `i`)
