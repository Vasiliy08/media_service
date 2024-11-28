from functools import lru_cache

from punq import Container, Scope

from src.infrastructure.cloude_s3.cloude import S3Client
from src.settings.config import Settings
from src.infrastructure.repositories.media import MediaRepository


@lru_cache(1)
def init_container():
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Settings, instance=Settings(), scope=Scope.singleton)
    settings: Settings = container.resolve(Settings)

    container.register(MediaRepository, scope=Scope.singleton)

    def create_cloud_storage():
        return S3Client(
            aws_access_key_id = settings.cloud.aws_access_key_id,
            aws_secret_access_key = settings.cloud.aws_secret_access_key,
            endpoint_url = settings.cloud.endpoint_url,
            bucket_name = settings.cloud.bucket_name,
        )

    container.register(S3Client, factory=create_cloud_storage, scope=Scope.singleton)

    return container