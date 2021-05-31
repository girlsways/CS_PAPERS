from __future__ import annotations

import typing as t
from datetime import datetime

from django.contrib import admin, messages
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _, ngettext
from jwcrypto.common import json_decode

from django_g