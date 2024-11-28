from dataclasses import dataclass
from aiobotocore.session import get_session


@dataclass
class S3Client:
    aws_access_key_id: str
    aws_secret_access_key: str
    endpoint_url: str
    bucket_name: str
    session = get_session()

    # Заглушка, S3 Селектел

    # @asynccontextmanager
    # async def get_client(self):
    #     async with self.session.create_client("s3",
    #         self.aws_access_key_id,
    #         self.aws_secret_access_key,
    #         self.endpoint_url,
    # ) as client:
    #         yield client

    async def upload_file(self, file: str):
        print("S3")
        # file_location = settings.UPLOAD_DIRECTORY / file.filename
        # async with self.get_client() as client:
        #     async with aiofiles.open(file_location, "rb") as out_file:
        #         await client.put_object(Bucket=self.bucket_name, Key=file.filename, Body=out_file,)
