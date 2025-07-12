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
    MINIO_SOURCE_BUCKET_NAME: str = ENVIRONMENT_VARIABLES.get("MINIO_SOURCE_BUCKET_NAME")
    MINIO_DESTINATION_BUCKET_NAME: str = ENVIRONMENT_VARIABLES.get("MINIO_DESTINATION_BUCKET_NAME")
    # MINIO_SECURE_CONNECTION: bool = bool(ENVIRONMENT_VARIABLES.get("MINIO_SECURE_CONNECTION"))

    INPUT_DIRECTORY_PATH = Path(ENVIRONMENT_VARIABLES.get("INPUT_DIRECTORY_PATH", ".."))
    OUTPUT_DIRECTORY_PATH: Path = Path(ENVIRONMENT_VARIABLES.get("OUTPUT_DIRECTORY_PATH", ".."))


class DatasetIOConfiguration:
    def __init__(self, file_name: str | Path):
        self.file_name = file_name

class DatasetPathConfiguration:

    STUDY_PROGRAMS_INPUT: Path = Path(ENVIRONMENT_VARIABLES.get("STUDY_PROGRAMS_DATA_INPUT_FILE_NAME"))
    STUDY_PROGRAMS_OUTPUT: Path = Path(ENVIRONMENT_VARIABLES.get("STUDY_PROGRAMS_DATA_OUTPUT_FILE_NAME"))

    COURSES_INPUT: Path = Path(ENVIRONMENT_VARIABLES.get("COURSES_DATA_INPUT_FILE_NAME"))
    COURSES_OUTPUT: Path = Path(ENVIRONMENT_VARIABLES.get("COURSES_DATA_OUTPUT_FILE_NAME"))

    PROFESSORS_INPUT: Path = Path(ENVIRONMENT_VARIABLES.get("PROFESSORS_DATA_INPUT_FILE_NAME"))
    PROFESSORS_OUTPUT: Path = Path(ENVIRONMENT_VARIABLES.get("PROFESSORS_DATA_OUTPUT_FILE_NAME"))

    CURRICULA_INPUT: Path = Path(ENVIRONMENT_VARIABLES.get("CURRICULA_DATA_INPUT_FILE_NAME"))
    CURRICULA_OUTPUT: Path = Path(ENVIRONMENT_VARIABLES.get("CURRICULA_DATA_OUTPUT_FILE_NAME"))

    REQUISITES_INPUT: Path = Path(ENVIRONMENT_VARIABLES.get("REQUISITES_DATA_INPUT_FILE_NAME"))
    REQUISITES_OUTPUT: Path = Path(ENVIRONMENT_VARIABLES.get("REQUISITES_DATA_OUTPUT_FILE_NAME"))

    OFFERS_INPUT: Path = Path(ENVIRONMENT_VARIABLES.get("OFFERS_DATA_INPUT_FILE_NAME"))
    OFFERS_OUTPUT: Path = Path(ENVIRONMENT_VARIABLES.get("OFFERS_DATA_OUTPUT_FILE_NAME"))

    INCLUDES_INPUT: Path = Path(ENVIRONMENT_VARIABLES.get("INCLUDES_DATA_INPUT_FILE_NAME"))
    INCLUDES_OUTPUT: Path = Path(ENVIRONMENT_VARIABLES.get("INCLUDES_DATA_OUTPUT_FILE_NAME"))

    REQUIRES_INPUT: Path = Path(ENVIRONMENT_VARIABLES.get("REQUIRES_DATA_INPUT_FILE_NAME"))
    REQUIRES_OUTPUT: Path = Path(ENVIRONMENT_VARIABLES.get("REQUIRES_DATA_OUTPUT_FILE_NAME"))

    SATISFIES_INPUT: Path = Path(ENVIRONMENT_VARIABLES.get("SATISFIES_DATA_INPUT_FILE_NAME"))
    SATISFIES_OUTPUT: Path = Path(ENVIRONMENT_VARIABLES.get("SATISFIES_DATA_OUTPUT_FILE_NAME"))

    TEACHES_INPUT: Path =  Path(ENVIRONMENT_VARIABLES.get("TEACHES_DATA_INPUT_FILE_NAME"))
    TEACHES_OUTPUT: Path = Path(ENVIRONMENT_VARIABLES.get("TEACHES_DATA_OUTPUT_FILE_NAME"))


class DatasetTransformationConfiguration:
    def __init__(self, columns: list[str]):
        self.columns = columns

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
                 input_io_config: DatasetIOConfiguration,
                 output_io_config: DatasetIOConfiguration,
                 transformation_config: DatasetTransformationConfiguration,
                 ):
        self.dataset_name = dataset
        self.input_io_config = input_io_config
        self.output_io_config = output_io_config
        self.transformation_config = transformation_config



DatasetConfiguration.STUDY_PROGRAMS = DatasetConfiguration(
    dataset=DatasetType.STUDY_PROGRAMS,
    input_io_config=DatasetIOConfiguration(DatasetPathConfiguration.STUDY_PROGRAMS_INPUT),
    output_io_config=DatasetIOConfiguration(DatasetPathConfiguration.STUDY_PROGRAMS_OUTPUT),
    transformation_config=DatasetTransformationConfiguration(
        columns=[
            "study_program_id",
            "study_program_code",
            "study_program_name",
            "study_program_duration",
            "study_program_url"
        ]
    )
)

DatasetConfiguration.COURSES = DatasetConfiguration(
    dataset=DatasetType.COURSES,
    input_io_config=DatasetIOConfiguration(DatasetPathConfiguration.COURSES_INPUT),
    output_io_config=DatasetIOConfiguration(DatasetPathConfiguration.COURSES_OUTPUT),
    transformation_config=DatasetTransformationConfiguration(
        columns=
        [
            "course_id",
            "course_code",
            "course_name_mk",
            "course_name_en",
            "course_url",
            "course_level"
        ]
    )
)

DatasetConfiguration.PROFESSORS = DatasetConfiguration(
    dataset=DatasetType.PROFESSORS,
    input_io_config=DatasetIOConfiguration(DatasetPathConfiguration.PROFESSORS_INPUT),
    output_io_config=DatasetIOConfiguration(DatasetPathConfiguration.PROFESSORS_OUTPUT),
    transformation_config=DatasetTransformationConfiguration(
        columns=
        [
            "professor_id",
            "professor_name",
            "professor_surname"
        ],
    )
)

DatasetConfiguration.CURRICULA = DatasetConfiguration(
    dataset=DatasetType.CURRICULA,
    input_io_config=DatasetIOConfiguration(DatasetPathConfiguration.CURRICULA_INPUT),
    output_io_config=DatasetIOConfiguration(DatasetPathConfiguration.CURRICULA_OUTPUT),
    transformation_config=DatasetTransformationConfiguration(
        columns=
        [
            "curriculum_id",
            "course_type",
            "course_semester_season",
            "course_academic_year",
            "course_semester"
        ]
    )
)

DatasetConfiguration.REQUISITES = DatasetConfiguration(
    dataset=DatasetType.REQUISITES,
    input_io_config=DatasetIOConfiguration(DatasetPathConfiguration.REQUISITES_INPUT),
    output_io_config=DatasetIOConfiguration(DatasetPathConfiguration.REQUISITES_OUTPUT),
    transformation_config=DatasetTransformationConfiguration(
        columns=
        [
            "requisite_id",
            "course_prerequisite_type",
            "minimum_required_number_of_courses"
        ],
    )
)
DatasetConfiguration.OFFERS = DatasetConfiguration(
    dataset=DatasetType.OFFERS,
    input_io_config=DatasetIOConfiguration(DatasetPathConfiguration.OFFERS_INPUT),
    output_io_config=DatasetIOConfiguration(DatasetPathConfiguration.OFFERS_OUTPUT),
    transformation_config=DatasetTransformationConfiguration(
        columns=
        [
            "offers_id",
            "curriculum_id",
            "study_program_id"
        ]
    )
)
DatasetConfiguration.INCLUDES = DatasetConfiguration(
    dataset=DatasetType.INCLUDES,
    input_io_config=DatasetIOConfiguration(DatasetPathConfiguration.INCLUDES_INPUT),
    output_io_config=DatasetIOConfiguration(DatasetPathConfiguration.INCLUDES_OUTPUT),
    transformation_config=DatasetTransformationConfiguration(
        columns=
        [
            "includes_id",
            "curriculum_id",
            "course_id"
        ]
    )
)
DatasetConfiguration.REQUIRES = DatasetConfiguration(
    dataset=DatasetType.POSTREQUISITES,
    input_io_config=DatasetIOConfiguration(DatasetPathConfiguration.REQUIRES_INPUT),
    output_io_config=DatasetIOConfiguration(DatasetPathConfiguration.REQUIRES_OUTPUT),
    transformation_config=DatasetTransformationConfiguration(
        columns=
        [
            "requires_id",
            "course_id",
            "requisite_id"
        ],
    )
)
DatasetConfiguration.SATISFIES = DatasetConfiguration(
    dataset=DatasetType.PREREQUISITES,
    input_io_config=DatasetIOConfiguration(DatasetPathConfiguration.SATISFIES_INPUT),
    output_io_config=DatasetIOConfiguration(DatasetPathConfiguration.SATISFIES_OUTPUT),
    transformation_config=DatasetTransformationConfiguration(
        columns=
        [
            "satisfies_id",
            "prerequisite_course_id",
            "requisite_id"
        ],
    )
)
DatasetConfiguration.TEACHES = DatasetConfiguration(
    dataset=DatasetType.TEACHES,
    input_io_config=DatasetIOConfiguration(DatasetPathConfiguration.TEACHES_INPUT),
    output_io_config=DatasetIOConfiguration(DatasetPathConfiguration.TEACHES_OUTPUT),
    transformation_config=DatasetTransformationConfiguration(
        columns=
        [
            "teaches_id",
            "course_id",
            "professor_id"
        ],
    )
)
