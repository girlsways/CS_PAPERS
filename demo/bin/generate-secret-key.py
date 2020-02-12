
#!/usr/bin/env python
import argparse
import typing as t
from pathlib import Path

from django.core.management.utils import get_random_secret_key

if t.TYPE_CHECKING:
    from io import StringIO

BASE_DIR = Path(__file__).parent.parent.resolve()


def main():
    parser = argparse.ArgumentParser(
        prog="generate-secret-key",
        description="Generate a secret key and optionally store it in an"
        " environment file.",
    )
    parser.add_argument(
        "--dotenv",
        help="Append to dotenv file at provided location",
        type=argparse.FileType(mode="at", encoding="utf-8"),
        metavar="envfile",
    )
    opts = parser.parse_args()
    key = get_random_secret_key()
    if not opts.dotenv:
        print(key)
        return

    file_obj: StringIO = opts.dotenv
    with file_obj:
        file_obj.writelines([f"SECRET_KEY='{key}'"])
        print(f"Secret key written to {file_obj.name}")


if __name__ == "__main__":
    main()