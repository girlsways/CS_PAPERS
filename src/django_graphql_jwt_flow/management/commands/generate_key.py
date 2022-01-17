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
            raise CommandError(f"Unsupported format: {options['priv_format']}")

        key = jwk.JWK.generate(kty="OKP", crv="Ed25519")
        if not options["pub_out"] and not options["priv_out"]:
            print("Private:")
            print(key.export_private())
            print("Public:")
            print(key.export_public())
            return

        if options["pub_out"]:
            self.write_public_key(key, options["pub_out"], options["pub_format"])

        if options["priv_out"]:
            self.write_private_key(key, options["priv_out"], options["priv_format"])

    def write_public_key(self, key: jwk.JWK, file_obj: StringIO, fmt: str):
        if fmt == "JSON":
            with file_obj:
                file_obj.write(key.export_public())
        elif fmt == "PEM":
            with file_obj:
                file_obj.write(key.export_to_pem().decode(self.encoding))
        else:
            self.stderr.write(self.style.ERROR(f"{fmt}: Unsupported format"))
            return
        self.stdout.write(self.style.SUCCESS("==> Public key exported."))

    def write_private_key(self, key: jwk.JWK, file_obj: StringIO, fmt: str):
        if fmt == "JSON":
            with file_obj:
                file_obj.write(key.export_private())
        elif fmt == "PEM":
            with file_obj:
                file_obj.write(
                    key.export_to_pem(private_key=True, password=None).decode(
                        self.encoding
                    )
                )
        else:
            self.stderr.write(self.style.ERROR(f"{fmt}: Unsupported format"))
            retur