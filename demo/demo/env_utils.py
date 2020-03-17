import os
import typing as t
from pathlib import Path


def get_list(name, separator=":") -> t.List[str]:
    return os.getenv(name, "").split(separator)


def yesno(name, default: str = "no") -> bool:
    return os.getenv(name, default).lower() in ["yes", "1", "true"]


def get(name, default: str = "") -> str:
    return os.getenv(name, default)


def get_path(name, must_exist=False, absolute=True) -> t.Optional[Path]:
    path_name = os.getenv(name, "")
    if path_name:
        path = Path(path_name)
        if must_exist and not path.exists():
            return None

        return 