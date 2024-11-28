from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy import BigInteger, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class MediaFile(Base):
    __tablename__ = "media_files"

    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    original_name: Mapped[str] = mapped_column(nullable=True)
    size: Mapped[int] = mapped_column(BigInteger, nullable=True)
    file_format: Mapped[str] = mapped_column(nullable=True)
    extension: Mapped[str] = mapped_column(nullable=True)
    last_downloaded: Mapped[datetime] = mapped_column(
        server_default=func.now(), server_onupdate=func.now()
    )
