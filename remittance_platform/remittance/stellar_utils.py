# stellar_utils.py

from stellar_sdk import Server
from django.conf import settings

server = Server(horizon_url=settings.STELLAR_HORIZON_URL)