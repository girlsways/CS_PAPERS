from collections import namedtuple

semantic = namedtuple("semantic", ["major", "minor", "patch"])
__VERSION__ = "0.0.0"


def get_version():
    defaults = (0, 0, 0)
    actual = __VERSION__.split(".", 2)
    parts = [
        actual[i] if i < len(actual) else defaults[i] for i 