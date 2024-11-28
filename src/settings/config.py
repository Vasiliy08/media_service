from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, PostgresDsn
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings


LOG_DEFAULT_FORMAT = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"


class LoggingConfig(BaseModel):
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = LOG_DEFAULT_FORMAT


class DatabaseConfig(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Cloud(BaseException):
    aws_access_key_id: str = Field(alias='AWS_ACCESS_KEY_ID')
    aws_secret_access_key:str = Field(alias='AWS_SECRET_ACCESS_KEY')
    endpoint_url: str = Field(alias='ENDPOINT_URL')
    bucket_name: str = Field(alias='BUCKET_NAME')
    

class Settings(BaseSettings):
    logger: LoggingConfig = LoggingConfig()
    db_config: DatabaseConfig = DatabaseConfig()
    cloud: Cloud = Cloud()
    
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    UPLOAD_DIRECTORY: Path = BASE_DIR / "uploads"


settings = Settings()