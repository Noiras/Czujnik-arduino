import json
from pathlib import Path
from pydantic import BaseModel


class ButtonConfig(BaseModel):
    text: str
    color: str
    color_active: str
    text_color: str
    width: int
    height: int
    radius: int
    font_family: str
    font_size: int


class Config(BaseModel):
    db_path: Path
    com_port: str
    baud_rate: int
    save_button: ButtonConfig


def load_config(path: str = "config.json") -> Config:
    with open(path) as f:
        return Config(**json.load(f))
