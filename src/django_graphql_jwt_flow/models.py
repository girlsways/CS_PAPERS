from __future__ import annotations

import typing as t
from datetime import datetime, timedelta
from json.decoder import JSONDecodeError

from django.contrib.auth import get_user_model
from django.db import models, IntegrityError
from django.utils.translation im