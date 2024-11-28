import datetime
from uuid import UUID
import aiofiles
from fastapi import UploadFile
from sqlalchemy import desc, func, select
from src.exceptions.media import FileNotFoundException
from src.infrastructure.converters import convert_upload_file_to_model_media_file
from src.infrastructure.models.media import MediaFile
from src.settings.config import settings
from src.infrastructure.repositories.db_helper import DatabaseHelper


class MediaRepository(DatabaseHelper):
    async def save_file_to_disk(self, file: UploadFile):
        file_location = settings.UPLOAD_DIRECTORY / file.filename
        async with aiofiles.open(file_location, "wb") as out_file:
            while content := await file.read(1024 * 1024):
                await out_file.write(content)
        print("ДИСК")

    async def save_file_to_db(self, file: UploadFile):
        async with self.session_factory() as session:
            media_file = await convert_upload_file_to_model_media_file(file=file)
            session.add(media_file)
            await session.commit()
        print("БД")

    async def get_file_by_uuid(self, uuid: UUID):
        async with self.session_factory() as session:
            media_file = await session.execute(
                select(MediaFile).where(MediaFile.uuid == uuid)
            )
            media_file = media_file.scalar_one_or_none()
            if media_file is None:
                raise FileNotFoundException(uuid=uuid)
            return media_file

    async def update_last_download(self, uuid: UUID):
        async with self.session_factory() as session:
            media_file = await session.execute(
                select(MediaFile).where(MediaFile.uuid == uuid)
            )
            media_file = media_file.scalar_one_or_none()
            if media_file is None:
                raise FileNotFoundException(uuid=uuid)
            media_file.last_downloaded = datetime.datetime.now()
            await session.commit()

    async def response_file(self, filename: str):
        file_path = settings.UPLOAD_DIRECTORY / filename
        async with aiofiles.open(file_path, "rb") as file:
            while chunk := await file.read(1024 * 1024):  # 1 МБ
                yield chunk

    async def delete_unused_files(self):
        current_time = datetime.datetime.now()
        unused_time_limit = datetime.timedelta(days=settings.FILE_EXPIRATION_DAYS)

        async with self.session_factory() as session:
            result = await session.execute(select(MediaFile))
            files = result.scalars().all()

            for file in files:
                if current_time - file.last_downloaded > unused_time_limit:
                    file_path = settings.UPLOAD_DIRECTORY / file.original_name
                    if file_path.exists():
                        file_path.unlink()
                        await session.delete(file)
                        await session.commit()

    async def get_all_files(self, pagination):
        async with self.session_factory() as session:
            query = select(MediaFile).limit(pagination.limit).offset(pagination.offset)
            if pagination.order_by == "asc":
                files = await session.execute(query)
                return files.scalars().all()
            files = await session.execute(query.order_by(desc(MediaFile.last_downloaded)))
            return files.scalars().all()
        
    async def get_count_files(self):
        async with self.session_factory() as session:
            count = await session.scalar(select(func.count()).select_from(MediaFile))
            return count