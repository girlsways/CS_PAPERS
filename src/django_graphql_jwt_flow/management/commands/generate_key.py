from __future__ import annotations

import argparse
import typing as t

import jwcrypto.jwk as jwk
from django.core.management import BaseCommand, CommandError

if t.TYPE_CHECKING:
    from io import StringIO


class Command(BaseCommand):
    encoding = "utf-8"
    supported_formats = ("PEM", "JSON")

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            "--pub-out",
            type=argparse.FileType(mode="wt", encoding=self.encoding),
            metavar="file",
            help="File to write the public key to.",
        )
        parser.add_argument("--pub-format", default="JSON")
        parser.add_argument(
            "--priv-out",
            type=argparse.FileType(mode="wt", encoding=self.encoding),
            metavar="file",
            help="File to write the private key to",
        )
        parser.add_argument("--priv-format", default="PEM")

    def handle(self, *args, **options):
        if options["pub_format"] not in self.supported_formats:
            raise CommandError(f"Unsupported format: {options['pub_format']}")
        if options["priv_format"] not in self.supported_formats:
         