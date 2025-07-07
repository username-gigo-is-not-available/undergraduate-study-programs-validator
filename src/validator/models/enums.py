from enum import StrEnum, auto


class UpperStrEnum(StrEnum):
    def _generate_next_value_(name, start, count, last_values):
        return name.upper()


class StageType(UpperStrEnum):
    LOAD = auto()
    VALIDATE = auto()
    STORE = auto()

class CourseType(UpperStrEnum):
    MANDATORY = auto()
    ELECTIVE = auto()

class CoursePrerequisiteType(UpperStrEnum):
    NONE: str = auto()
    ONE: str = auto()
    ANY: str = auto()
    TOTAL: str = auto()

class CourseSemesterSeasonType(UpperStrEnum):
    WINTER: str = auto()
    SUMMER: str = auto()

class OperatorType(UpperStrEnum):
    AND = auto()
    OR = auto()

class DatasetType(UpperStrEnum):
    STUDY_PROGRAMS: str = auto()
    COURSES: str = auto()
    PROFESSORS: str = auto()
    CURRICULA: str = auto()
    REQUISITES: str = auto()
    OFFERS: str = auto()
    INCLUDES: str = auto()
    PREREQUISITES: str = auto()
    POSTREQUISITES: str = auto()
    TEACHES: str = auto()