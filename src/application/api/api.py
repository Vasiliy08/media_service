import asyncio
from typing import Annotated
from uuid import UUID
import punq
from fastapi import HTTPException, Query, UploadFile, APIRouter, Depends, status
from fastapi.responses import StreamingResponse
from src.application.api.schemas import (
    ApiResponse,
    ErrorSchema,
    Files,
    ListPaginatedResponse,
    PaginationIn,
    PaginationOut,
)
from src.exceptions.base import ApplicationException
from src.infrastructure.cloude_s3.cloude import S3Client
from src.infrastructure.repositories.media import MediaRepository
from src.infrastructure.di import init_container

router = APIRouter(tags=[""])


@router.post(
    "/upload/",
    status_code=status.HTTP_201_CREATED,
    description="Эндпоинт для загрузки файла на локальный диск, S3, и метаданных в БД",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def upload_file(
    file: UploadFile,
    container: Annotated[punq.Container, Depends(init_container)],
):
    media_container: MediaRepository = container.resolve(MediaRepository)
    cloud_container: S3Client = container.resolve(S3Client)
    # Смотрим логи, все сервисы (S3, БД, Диск) отработали асинхронно
    await asyncio.gather(
        media_container.save_file_to_disk(file),
        media_container.save_file_to_db(file),
        cloud_container.upload_file(file),
    )

    return {"message": "Файл успешно загружен"}


@router.get(
    "/download/{uuid}/",
    status_code=status.HTTP_201_CREATED,
    description="Эндпоинт для скачивания файла",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def download_file(
    uuid: UUID,
    container: Annotated[punq.Container, Depends(init_container)],
):
    container: MediaRepository = container.resolve(MediaRepository)
    try:
        file = await container.get_file_by_uuid(uuid)
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    await container.update_last_download(uuid)
    iter_file = container.response_file(file.original_name)

    return StreamingResponse(iter_file, media_type="application/octet-stream")


@router.get(
    "/files/",
    response_model=ApiResponse[ListPaginatedResponse[Files]],
    status_code=status.HTTP_200_OK,
    description="Получить список всех файлов c возможностью пагинации и сортировки по полю последней загрузки",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def get_all_files(
    pagination: Annotated[PaginationIn, Query()],
    container: Annotated[punq.Container, Depends(init_container)],
):
    container: MediaRepository = container.resolve(MediaRepository)

    files = await container.get_all_files(pagination)
    count = await container.get_count_files()

    return ApiResponse(
        data=ListPaginatedResponse(
            items=files,
            pagination=PaginationOut(
                page=pagination.offset,
                limit=pagination.limit,
                total=count,
                order_by=pagination.order_by,
            ),
        )
    )
