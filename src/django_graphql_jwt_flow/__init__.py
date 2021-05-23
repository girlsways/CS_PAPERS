from collections import namedtuple

semantic = namedtuple("semantic", ["major", "minor", "patch"])
__VERSION__ = "0.0.0"


def get_version():
    def