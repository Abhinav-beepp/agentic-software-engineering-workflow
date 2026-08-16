import secrets
import string
from urllib.parse import urlparse

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import CollisionError, NotFoundError
from app.storage.models import URLRecord
from app.storage.repository import URLRepository


class URLService:
    def __init__(self, session: Session, code_length: int = 7) -> None:
        self.repo = URLRepository(session)
        self.code_length = code_length

    def create(self, original_url: str) -> URLRecord:
        self._validate_url(original_url)
        for _ in range(5):
            code = self._generate_code()
            if self.repo.get_by_code(code):
                continue
            try:
                return self.repo.create(original_url, code)
            except IntegrityError:
                self.repo.session.rollback()
        raise CollisionError("Could not allocate a unique short code")

    def resolve(
        self,
        short_code: str,
        user_agent: str | None = None,
        referrer: str | None = None,
    ) -> URLRecord:
        record = self.repo.get_by_code(short_code)
        if record is None:
            raise NotFoundError("Short URL not found")
        self.repo.record_click(record, user_agent, referrer)
        return record

    def analytics(self, short_code: str) -> URLRecord:
        record = self.repo.get_by_code(short_code)
        if record is None:
            raise NotFoundError("Short URL not found")
        return record

    def _generate_code(self) -> str:
        alphabet = string.ascii_letters + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(self.code_length))

    @staticmethod
    def _validate_url(value: str) -> None:
        parsed = urlparse(value)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("Only valid HTTP(S) URLs are supported")
