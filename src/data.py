import pydantic
import sqlite3
import data_structs
import datetime
from pathlib import Path


def initalize(path: str) -> None:
    if not Path(path).exists():
        raise FileNotFoundError(f"Nie ma pliku z lokalizacja: {path}")

    with sqlite3.connect(path) as con:
        con.execute(
            "CREATE TABLE IF NOT EXISTS dane (temperatura, cisnienie, wilgotnosc)"
        )
        con.commit()


def get_con(path: str):
    return sqlite3.Connection(path)


def put_data(db: sqlite3.Connection, data: data_structs.Struct):
    dane = data.model_dump(exclude_none=True).values()
    data_pomiaru = datetime.datetime.now().isoformat()
    db.execute(
        "INSERT INTO dane (temperatura, wilgotnosc, cisnienie, data_pomiaru) with (?, ?, ?, ?)",
        (dane["temperatura"], dane["cisnienie"], dane["wilgotnosc"], data_pomiaru),
    )
    db.commit()


# struct update musi miec datę wiec problem z glowy
def get_data(
    db: sqlite3.Connection, struct: data_structs.StructUpdate
) -> list[data_structs.Struct]:
    data = struct.data_pomiaru
    rows = db.execute("SELECT * FROM dane WHERE data=?", (data,)).fetchall()
    return [
        data_structs.Struct(temperatura=r[0], cisnienie=r[1], wilgotnosc=r[2])
        for r in rows
    ]
