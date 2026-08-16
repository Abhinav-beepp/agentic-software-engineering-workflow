"""Representative generated service artifact.

This artifact is intentionally deterministic for the interview demo. The production-
runnable implementation lives in src/app/services/url_service.py and is tested by
pytest. The workflow therefore demonstrates code generation without executing
untrusted generated source.
"""

from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True)
class ShortUrlDraft:
    original_url: str
    short_code: str


def validate_http_url(value: str) -> str:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("original_url must be an absolute HTTP(S) URL")
    return value


def build_short_url(base_url: str, short_code: str) -> str:
    return f"{base_url.rstrip('/')}/{short_code}"
