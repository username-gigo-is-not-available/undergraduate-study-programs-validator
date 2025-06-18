import os
import re
from pathlib import Path

from dotenv import dotenv_values


class Config:
    ECTS_VALUE: int = 6
    PROFESSOR_TITLES: list[str] = ["ворн.", "проф.", "д-р", "доц."]
    COURSE_CODE_REGEX: re.Pattern[str] = re.compile(r'^F23L[1-3][SW]\d{3}$')
    STUDY_PROGRAM_CODE_REGEX: re.Pattern[str] = re.compile(r'^[A-Z]{2,4}\d{1}$')

    ENVIRONMENT_VARIABLES: dict[str, str] = {**dotenv_values('../.env'), **os.environ}

    FILE_STORAGE_TYPE: str = ENVIRONMENT_VARIABLES.get('FILE_STORAGE_TYPE')
    MINIO_ENDPOINT_URL: str = ENVIRONMENT_VARIABLES.get('MINIO_ENDPOINT_URL')
    MINIO_ACCESS_KEY: str = ENVIRONMENT_VARIABLES.get('MINIO_ACCESS_KEY')
    MINIO_SECRET_KEY: str = ENVIRONMENT_VARIABLES.get('MINIO_SECRET_KEY')
    MINIO_SOURCE_BUCKET_NAME: str = ENVIRONMENT_VARIABLES.get('MINIO_SOURCE_BUCKET_NAME')
    MINIO_DESTINATION_BUCKET_NAME: str = ENVIRONMENT_VARIABLES.get('MINIO_DESTINATION_BUCKET_NAME')
    # MINIO_SECURE_CONNECTION: bool = bool(ENVIRONMENT_VARIABLES.get('MINIO_SECURE_CONNECTION'))

    INPUT_DIRECTORY_PATH = Path(ENVIRONMENT_VARIABLES.get('INPUT_DIRECTORY_PATH', '..'))
    OUTPUT_DIRECTORY_PATH: Path = Path(ENVIRONMENT_VARIABLES.get('OUTPUT_DIRECTORY_PATH', '..'))

    STUDY_PROGRAMS_INPUT_FILE_NAME: Path = Path(ENVIRONMENT_VARIABLES.get('STUDY_PROGRAMS_DATA_INPUT_FILE_NAME'))
    STUDY_PROGRAMS_COLUMN_ORDER: list[str] = [
        'study_program_id',
        'study_program_code',
        'study_program_name',
        'study_program_duration',
        'study_program_url'
    ]
    STUDY_PROGRAMS_OUTPUT_FILE_NAME: Path = Path(ENVIRONMENT_VARIABLES.get('STUDY_PROGRAMS_DATA_OUTPUT_FILE_NAME'))
    COURSES_INPUT_FILE_NAME: Path = Path(ENVIRONMENT_VARIABLES.get('COURSES_DATA_INPUT_FILE_NAME'))
    COURSES_COLUMN_ORDER: list[str] = [
        'course_id',
        'course_code',
        'course_name_mk',
        'course_name_en',
        'course_url',
    ]
    COURSES_OUTPUT_FILE_NAME: Path = Path(ENVIRONMENT_VARIABLES.get('COURSES_DATA_OUTPUT_FILE_NAME'))
    PROFESSORS_INPUT_FILE_NAME: Path = Path(ENVIRONMENT_VARIABLES.get('PROFESSORS_DATA_INPUT_FILE_NAME'))
    PROFESSORS_COLUMN_ORDER: list[str] = [
        'professor_id',
        'professor_name',
        'professor_surname'
    ]
    PROFESSORS_OUTPUT_FILE_NAME: Path = Path(ENVIRONMENT_VARIABLES.get('PROFESSORS_DATA_OUTPUT_FILE_NAME'))


    TEACHES_INPUT_FILE_NAME: Path = Path(ENVIRONMENT_VARIABLES.get('TEACHES_DATA_INPUT_FILE_NAME'))
    TEACHES_COLUMN_ORDER: list[str] = [
        'teaches_id',
        'course_id',
        'professor_id'
    ]
    TEACHES_OUTPUT_FILE_NAME : Path = Path(ENVIRONMENT_VARIABLES.get('TEACHES_DATA_OUTPUT_FILE_NAME'))
    OFFERS_INPUT_FILE_NAME: Path = Path(ENVIRONMENT_VARIABLES.get('OFFERS_DATA_INPUT_FILE_NAME'))
    OFFERS_COLUMN_ORDER: list[str] = [
        'offers_id',
        'study_program_id',
        'course_id',
        'course_type',
        'course_semester',
        'course_semester_season',
        'course_academic_year',
        'course_level',
    ]
    OFFERS_OUTPUT_FILE_NAME : Path = Path(ENVIRONMENT_VARIABLES.get('OFFERS_DATA_OUTPUT_FILE_NAME'))
    REQUIRES_INPUT_FILE_NAME: Path = Path(ENVIRONMENT_VARIABLES.get('REQUIRES_DATA_INPUT_FILE_NAME'))
    REQUIRES_COLUMN_ORDER: list[str] = [
        'requires_id',
        'course_id',
        'course_prerequisite_type',
        'course_prerequisite_id',
        'minimum_required_number_of_courses',
    ]
    REQUIRES_OUTPUT_FILE_NAME: Path = Path(ENVIRONMENT_VARIABLES.get('REQUIRES_DATA_OUTPUT_FILE_NAME'))
