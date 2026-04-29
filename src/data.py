import pydantic
import sqlite3
import data_structs
import datetime
from pathlib import Path


def initalize(path: str) -> None:
    with sqlite3.connect(path) as con:
        con.execute(
            "CREATE TABLE IF NOT EXISTS dane (temperatura REAL, cisnienie REAL, wilgotnosc INTEGER, data_pomiaru TEXT)"
        )
        con.commit()


def get_con(path: str):
    return sqlite3.Connection(path)


def put_data(db: sqlite3.Connection, data: data_structs.Struct):
    dane = data.model_dump(exclude_none=True)
    data_pomiaru = datetime.datetime.now().isoformat()
    db.execute(
        "INSERT INTO dane (temperatura, cisnienie, wilgotnosc, data_pomiaru) VALUES (?, ?, ?, ?)",
        (dane["temperatura"], dane["cisnienie"], dane["wilgotnosc"], data_pomiaru),
    )
    db.commit()


def get_all(db: sqlite3.Connection) -> list[data_structs.StructUpdate]:
    db.row_factory = sqlite3.Row
    rows = db.execute("SELECT * FROM dane").fetchall()
    return [data_structs.StructUpdate(**dict(r)) for r in rows]


def get_data(
    db: sqlite3.Connection, struct: data_structs.StructUpdate
) -> list[data_structs.Struct]:
    data = struct.data_pomiaru
    rows = db.execute("SELECT * FROM dane WHERE data=?", (data,)).fetchall()
    return [
        data_structs.Struct(temperatura=r[0], cisnienie=r[1], wilgotnosc=r[2])
        for r in rows
    ]
