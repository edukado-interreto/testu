from .base import *  # noqa

CSRF_TRUSTED_ORIGINS = ["https://*.testu.eu"]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
