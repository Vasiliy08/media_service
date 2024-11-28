from fastapi import UploadFile
from src.infrastructure.models.media import MediaFile


async def convert_upload_file_to_model_media_file(file: UploadFile):
    return MediaFile(
        original_name=file.filename,
        size=file.size,
        file_format=file.content_type,
        extension=file.filename.split(".")[-1],
    )
