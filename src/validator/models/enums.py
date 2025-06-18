from enum import StrEnum, auto


class UpperStrEnum(StrEnum):
    def _generate_next_value_(name, start, count, last_values):
        return name.upper()


class StageType(UpperStrEnum):
    LOADING = auto()
    SELECTING = auto()
    RENAMING = auto()
    FILTERING = auto()
    MERGING = auto()
    VALIDATING = auto()
    STORING = auto()


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