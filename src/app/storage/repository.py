from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import utcnow
from app.storage.models import ClickEvent, URLRecord


class URLRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, original_url: str, short_code: str) -> URLRecord:
        record = URLRecord(
            original_url=original_url,
            short_code=short_code,
        )
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return record

    def get_by_code(self, short_code: str) -> URLRecord | None:
        return self.session.scalar(select(URLRecord).where(URLRecord.short_code == short_code))

    def record_click(
        self,
        record: URLRecord,
        user_agent: str | None,
        referrer: str | None,
    ) -> None:
        now = utcnow()
        record.click_count += 1
        record.last_clicked_at = now
        self.session.add(
            ClickEvent(
                url_id=record.id,
                clicked_at=now,
                user_agent=user_agent,
                referrer=referrer,
            )
        )
        self.session.commit()
