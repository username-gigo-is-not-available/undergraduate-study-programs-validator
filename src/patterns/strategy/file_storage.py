import logging
from io import BytesIO
from pathlib import Path

import pandas as pd
from minio import S3Error, Minio

from src.clients import MinioClient
from src.configurations import StorageConfiguration


class FileStorageStrategy:
    def read_data(self, input_file_name: Path) -> pd.DataFrame:
        raise NotImplementedError

class LocalFileStorage(FileStorageStrategy):

    def read_data(self, input_file_name: Path) -> pd.DataFrame:
        try:
            return pd.read_csv(StorageConfiguration.INPUT_DIRECTORY_PATH / input_file_name)
        except FileNotFoundError as e:
            logging.error(f"File not found: {StorageConfiguration.INPUT_DIRECTORY_PATH  / input_file_name}, {e}")
            raise
        except Exception as e:
            logging.error(f"Failed to read data from local storage: {StorageConfiguration.INPUT_DIRECTORY_PATH } {e}")
            raise

class MinioFileStorage(FileStorageStrategy):

    def read_data(self, input_file_name: Path) -> pd.DataFrame:
        try:
            input_file_name: str = str(input_file_name)
            minio_client: Minio = MinioClient().connect()
            csv_bytes: bytes = minio_client.get_object(StorageConfiguration.MINIO_SOURCE_BUCKET_NAME , str(input_file_name)).read()
            csv_buffer: BytesIO = BytesIO(csv_bytes)
            return pd.read_csv(csv_buffer)
        except S3Error as e:
            logging.error(f"Failed to read data from MinIO bucket {StorageConfiguration.MINIO_SOURCE_BUCKET_NAME}: {e}")
            raise

