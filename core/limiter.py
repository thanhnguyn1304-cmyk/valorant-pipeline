"""
Rate Limiter — shared instance for the entire app.
Extracted to avoid circular imports between main.py and endpoint routers.
"""
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
