import os
import typing as t
from pathlib import Path


def get_list(name, separator=":") -> t.List[str]:
    return os.getenv(name, "").split(separator)


def yesno(name, default: str = "no") -> bool:
    return os.getenv(name, default).lower() in [