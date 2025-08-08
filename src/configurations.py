import os
import re
from pathlib import Path

from dotenv import dotenv_values

from src.validator.models.enums import CoursePrerequisiteType, CourseType, CourseSemesterSeasonType, DatasetType

ENVIRONMENT_VARIABLES: dict[str, str] = {**dotenv_values("../.env"), **os.environ}


class ApplicationConfiguration:
    ECTS_VALUE: int = 6
    PROFESSOR_TITLES: list[str] = ["ворн.", "проф.", "д-р", "доц."]
    VALID_STUDY_PROGRAM_CODE_REGEX: re.Pattern[str] = re.compile(r"^[A-Z]{2,4}\d{1}$")
    VALID_STUDY_PROGRAM_DURATIONS: set[int] = {2, 3, 4}
    VALID_COURSE_CODE_REGEX: re.Pattern[str] = re.compile(r"^F23L[1-3][SW]\d{3}$")
    VALID_COURSE_LEVELS: set[int] = {1, 2, 3}
    VALID_COURSE_PREREQUISITE_TYPES: set[CoursePrerequisiteType] = {CoursePrerequisiteType.ONE,
                                                                    CoursePrerequisiteType.ANY,
                                                                    CoursePrerequisiteType.TOTAL}
    VALID_MINIMUM_REQUIRED_NUMBER_OF_COURSES_RANGE: range = range(0, 39)
    VALID_COURSE_TYPES: set[CourseType] = {CourseType.MANDATORY, CourseType.ELECTIVE}
    VALID_COURSE_SEMESTER_SEASONS: set[CourseSemesterSeasonType] = {CourseSemesterSeasonType.WINTER,
                                                                    CourseSemesterSeasonType.SUMMER}
    VALID_COURSE_ACADEMIC_YEARS_RANGE: range = range(1, 4)
    VALID_COURSE_SEMESTERS_RANGE: range = range(1, 8)


class StorageConfiguration:
    FILE_STORAGE_TYPE: str = ENVIRONMENT_VARIABLES.get("FILE_STORAGE_TYPE")
    MINIO_ENDPOINT_URL: str = ENVIRONMENT_VARIABLES.get("MINIO_ENDPOINT_URL")
    MINIO_ACCESS_KEY: str = ENVIRONMENT_VARIABLES.get("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY: str = ENVIRONMENT_VARIABLES.get("MINIO_SECRET_KEY")
    MINIO_INPUT_DATA_BUCKET_NAME: str = ENVIRONMENT_VARIABLES.get("MINIO_INPUT_DATA_BUCKET_NAME")
    MINIO_SCHEMA_BUCKET_NAME: str = ENVIRONMENT_VARIABLES.get("MINIO_SCHEMA_BUCKET_NAME")
    # MINIO_SECURE_CONNECTION: bool = bool(ENVIRONMENT_VARIABLES.get("MINIO_SECURE_CONNECTION"))

    INPUT_DATA_DIRECTORY_PATH = Path(ENVIRONMENT_VARIABLES.get("INPUT_DATA_DIRECTORY_PATH", ".."))
    SCHEMA_DIRECTORY_PATH: Path = Path(ENVIRONMENT_VARIABLES.get('SCHEMA_DIRECTORY_PATH', '..'))


class DatasetIOConfiguration:
    def __init__(self, file_name: str | Path
                 ):
        self.file_name = file_name


class PathConfiguration:
    STUDY_PROGRAMS_INPUT_DATA: Path = Path(ENVIRONMENT_VARIABLES.get("STUDY_PROGRAMS_DATA_INPUT_FILE_NAME"))
    COURSES_INPUT_DATA: Path = Path(ENVIRONMENT_VARIABLES.get("COURSES_DATA_INPUT_FILE_NAME"))
    PROFESSORS_INPUT_DATA: Path = Path(ENVIRONMENT_VARIABLES.get("PROFESSORS_DATA_INPUT_FILE_NAME"))
    CURRICULA_INPUT_DATA: Path = Path(ENVIRONMENT_VARIABLES.get("CURRICULA_DATA_INPUT_FILE_NAME"))
    REQUISITES_INPUT_DATA: Path = Path(ENVIRONMENT_VARIABLES.get("REQUISITES_DATA_INPUT_FILE_NAME"))
    OFFERS_INPUT_DATA: Path = Path(ENVIRONMENT_VARIABLES.get("OFFERS_DATA_INPUT_FILE_NAME"))
    INCLUDES_INPUT_DATA: Path = Path(ENVIRONMENT_VARIABLES.get("INCLUDES_DATA_INPUT_FILE_NAME"))
    REQUIRES_INPUT_DATA: Path = Path(ENVIRONMENT_VARIABLES.get("REQUIRES_DATA_INPUT_FILE_NAME"))
    SATISFIES_INPUT_DATA: Path = Path(ENVIRONMENT_VARIABLES.get("SATISFIES_DATA_INPUT_FILE_NAME"))
    TEACHES_INPUT_DATA: Path = Path(ENVIRONMENT_VARIABLES.get("TEACHES_DATA_INPUT_FILE_NAME"))

    STUDY_PROGRAMS_SCHEMA: Path = Path(ENVIRONMENT_VARIABLES.get("STUDY_PROGRAMS_SCHEMA_FILE_NAME"))
    CURRICULA_SCHEMA: Path = Path(ENVIRONMENT_VARIABLES.get("CURRICULA_SCHEMA_FILE_NAME"))
    COURSES_SCHEMA: Path = Path(ENVIRONMENT_VARIABLES.get("COURSES_SCHEMA_FILE_NAME"))
    REQUISITES_SCHEMA: Path = Path(ENVIRONMENT_VARIABLES.get("REQUISITES_SCHEMA_FILE_NAME"))
    PROFESSORS_SCHEMA: Path = Path(ENVIRONMENT_VARIABLES.get("PROFESSORS_SCHEMA_FILE_NAME"))
    OFFERS_SCHEMA: Path = Path(ENVIRONMENT_VARIABLES.get("OFFERS_SCHEMA_FILE_NAME"))
    INCLUDES_SCHEMA: Path = Path(ENVIRONMENT_VARIABLES.get("INCLUDES_SCHEMA_FILE_NAME"))
    REQUIRES_SCHEMA: Path = Path(ENVIRONMENT_VARIABLES.get("REQUIRES_SCHEMA_FILE_NAME"))
    SATISFIES_SCHEMA: Path = Path(ENVIRONMENT_VARIABLES.get("SATISFIES_SCHEMA_FILE_NAME"))
    TEACHES_SCHEMA: Path = Path(ENVIRONMENT_VARIABLES.get("TEACHES_SCHEMA_FILE_NAME"))


class DatasetConfiguration:
    STUDY_PROGRAMS: "DatasetConfiguration"
    COURSES: "DatasetConfiguration"
    PROFESSORS: "DatasetConfiguration"
    CURRICULA: "DatasetConfiguration"
    REQUISITES: "DatasetConfiguration"
    OFFERS: "DatasetConfiguration"
    INCLUDES: "DatasetConfiguration"
    REQUIRES: "DatasetConfiguration"
    SATISFIES: "DatasetConfiguration"
    TEACHES: "DatasetConfiguration"

    def __init__(self,
                 dataset: DatasetType,
                 input_io_configuration: DatasetIOConfiguration,
                 schema_configuration: DatasetIOConfiguration,
                 ):
        self.dataset_name = dataset
        self.input_io_configuration = input_io_configuration
        self.schema_configuration = schema_configuration


DatasetConfiguration.STUDY_PROGRAMS = DatasetConfiguration(
    dataset=DatasetType.STUDY_PROGRAMS,
    input_io_configuration=DatasetIOConfiguration(PathConfiguration.STUDY_PROGRAMS_INPUT_DATA),
    schema_configuration=DatasetIOConfiguration(PathConfiguration.STUDY_PROGRAMS_SCHEMA),
)

DatasetConfiguration.CURRICULA = DatasetConfiguration(
    dataset=DatasetType.CURRICULA,
    input_io_configuration=DatasetIOConfiguration(PathConfiguration.CURRICULA_INPUT_DATA),
    schema_configuration=DatasetIOConfiguration(PathConfiguration.CURRICULA_SCHEMA),
)

DatasetConfiguration.COURSES = DatasetConfiguration(
    dataset=DatasetType.COURSES,
    input_io_configuration=DatasetIOConfiguration(PathConfiguration.COURSES_INPUT_DATA),
    schema_configuration=DatasetIOConfiguration(PathConfiguration.COURSES_SCHEMA),
)

DatasetConfiguration.REQUISITES = DatasetConfiguration(
    dataset=DatasetType.REQUISITES,
    input_io_configuration=DatasetIOConfiguration(PathConfiguration.REQUISITES_INPUT_DATA),
    schema_configuration=DatasetIOConfiguration(PathConfiguration.REQUISITES_SCHEMA),
)

DatasetConfiguration.PROFESSORS = DatasetConfiguration(
    dataset=DatasetType.PROFESSORS,
    input_io_configuration=DatasetIOConfiguration(PathConfiguration.PROFESSORS_INPUT_DATA),
    schema_configuration=DatasetIOConfiguration(PathConfiguration.PROFESSORS_SCHEMA),
)

DatasetConfiguration.OFFERS = DatasetConfiguration(
    dataset=DatasetType.OFFERS,
    input_io_configuration=DatasetIOConfiguration(PathConfiguration.OFFERS_INPUT_DATA),
    schema_configuration=DatasetIOConfiguration(PathConfiguration.OFFERS_SCHEMA),
)

DatasetConfiguration.INCLUDES = DatasetConfiguration(
    dataset=DatasetType.INCLUDES,
    input_io_configuration=DatasetIOConfiguration(PathConfiguration.INCLUDES_INPUT_DATA),
    schema_configuration=DatasetIOConfiguration(PathConfiguration.INCLUDES_SCHEMA),

)

DatasetConfiguration.REQUIRES = DatasetConfiguration(
    dataset=DatasetType.POSTREQUISITES,
    input_io_configuration=DatasetIOConfiguration(PathConfiguration.REQUIRES_INPUT_DATA),
    schema_configuration=DatasetIOConfiguration(PathConfiguration.REQUIRES_SCHEMA),

)

DatasetConfiguration.SATISFIES = DatasetConfiguration(
    dataset=DatasetType.PREREQUISITES,
    input_io_configuration=DatasetIOConfiguration(PathConfiguration.SATISFIES_INPUT_DATA),
    schema_configuration=DatasetIOConfiguration(PathConfiguration.SATISFIES_SCHEMA),

)

DatasetConfiguration.TEACHES = DatasetConfiguration(
    dataset=DatasetType.TEACHES,
    input_io_configuration=DatasetIOConfiguration(PathConfiguration.TEACHES_INPUT_DATA),
    schema_configuration=DatasetIOConfiguration(PathConfiguration.TEACHES_SCHEMA),
)
