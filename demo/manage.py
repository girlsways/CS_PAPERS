
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# PyCharm friendly: PyCharm doesn't execute main() before executing django.setup()
#                   so whatever is in .env isn't loaded yet if we put this
#                   code in main().
try:
    import dotenv
except ImportError:
    dotenv = None

if dotenv:
    dotenv.load_dotenv(dotenv.find_dotenv(".env", raise_error_if_not_found=True))

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()