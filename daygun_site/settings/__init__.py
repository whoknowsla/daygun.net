import os
from decouple import config

if config('DEBUG', default=False, cast=bool):
    from .base import *
else:
    from .production import *
