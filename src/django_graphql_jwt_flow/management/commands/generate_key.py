from __future__ import annotations

import argparse
import typing as t

import jwcrypto.jwk as jwk
from django.core.management import BaseCommand, CommandError

if t.TYPE_CHECKING:
    from io import StringIO


class Command(BaseCommand):
    encoding = "utf-8"
    supported_form