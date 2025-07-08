from pathlib import Path

import pandas as pd
from minio import Minio

from src.clients import MinioClient
from src.configurations import DatasetConfiguration, StorageConfiguration
from src.patterns.strategy.file_storage import LocalFileStorage, MinioFileStorage


class FileStorageMixin:
    def __init__(self):
        if StorageConfiguration.FILE_STORAGE_TYPE == 'LOCAL':
            if not StorageConfiguration.OUTPUT_DIRECTORY_PATH.exists():
                StorageConfiguration.OUTPUT_DIRECTORY_PATH.mkdir(parents=True)
            self.file_storage_strategy = LocalFileStorage()
        elif StorageConfiguration.FILE_STORAGE_TYPE == 'MINIO':
            minio_client: Minio = MinioClient().connect()
            if not minio_client.bucket_exists(StorageConfiguration.MINIO_DESTINATION_BUCKET_NAME):
                minio_client.make_bucket(StorageConfiguration.MINIO_DESTINATION_BUCKET_NAME)
            self.file_storage_strategy = MinioFileStorage()
        else:
            raise ValueError(f"Unsupported storage type: {StorageConfiguration.FILE_STORAGE_TYPE}")

    def read_data(self, configuration: DatasetConfiguration) -> pd.DataFrame:
        df: pd.DataFrame = self.file_storage_strategy.read_data(configuration.input_io_config.file_name)
        if configuration.transformation_config.columns:
            df = df[configuration.transformation_config.columns]
        return df

    def save_data(self, df: pd.DataFrame, configuration: DatasetConfiguration) -> pd.DataFrame:
        columns: list[str] = [col for col in configuration.transformation_config.columns if col in df.columns]
        df_copy: pd.DataFrame = df.copy()[columns]
        self.file_storage_strategy.save_data(df_copy, configuration.output_io_config.file_name)
        return df
