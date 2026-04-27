import json
from pathlib import Path
from pydantic import BaseModel


class Config(BaseModel):
    db_path: Path
    com_port: str
    baud_rate: int


def load_config(path: str = "config.json") -> Config:
    with open(path) as f:
        return Config(**json.load(f))
