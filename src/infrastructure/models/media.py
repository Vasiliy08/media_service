from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class MediaFile(Base):
    __tablename__ = "media_files"

    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    original_name: Mapped[str]
    size: Mapped[int]
    file_format: Mapped[str]
    extension: Mapped[str]