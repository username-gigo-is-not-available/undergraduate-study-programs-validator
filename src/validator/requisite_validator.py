import pandas as pd

from src.config import Config
from src.patterns.builder.pipeline import Pipeline
from src.patterns.builder.stage import PipelineStage
from src.patterns.builder.step import PipelineStep
from src.patterns.mixin.file_storage import FileStorageMixin
from src.patterns.strategy.filter import NotEqualFilteringStrategy, GroupExistsFilteringStrategy
from src.patterns.strategy.validator import ChoiceValidatorStrategy, RangeValidatorStrategy
from src.validator.models.enums import StageType, CoursePrerequisiteType


def requisite_validator(df_prerequisites: pd.DataFrame, df_offers: pd.DataFrame,
                        df_includes: pd.DataFrame) -> Pipeline:
    return (Pipeline(
        name='requisite-validator-pipeline'
    )
    .add_stage(
        PipelineStage(
            name='load-data',
            stage_type=StageType.LOADING
        )
        .add_step(
            PipelineStep(
                name='load-requisite-data',
                function=PipelineStep.read_data,
                input_file_location=PipelineStep.get_input_file_location(),
                input_file_name=Config.REQUISITES_INPUT_FILE_NAME,
                columns=Config.REQUISITES_COLUMNS,
            )
        )
    )
    .add_stage(
        PipelineStage(
            name='merge-data',
            stage_type=StageType.MERGING
        )
        .add_step(
            PipelineStep(
                name='merge-with-prerequisite-data',
                function=PipelineStep.merge,
                merge_df=df_prerequisites,
                on='requisite_id',
            )
        )
        .add_step(
            PipelineStep(
                name='merge-with-includes-data',
                function=PipelineStep.merge,
                merge_df=df_includes,
                left_on='course_prerequisite_id',
                right_on='course_id',
            )
        )
        .add_step(
            PipelineStep(
                name='merge-with-offers-data',
                function=PipelineStep.merge,
                merge_df=df_offers,
                on='curriculum_id'
            )
        )
    )
    .add_stage(
        PipelineStage(
            name='filter-data',
            stage_type=StageType.FILTERING,
        ).add_step(
            PipelineStep(
                name='filter-out-none-course-prerequisite-types',
                function=PipelineStep.filter,
                filter=NotEqualFilteringStrategy(column='course_prerequisite_type', value=CoursePrerequisiteType.NONE),
            )
        )
        .add_step(
            PipelineStep(
                name='filter-out-requisites-with-no-offers',
                function=PipelineStep.filter,
                filter=GroupExistsFilteringStrategy(group_by_columns=[
                    'study_program_id',
                    'course_prerequisite_id'
                ], evaluated_columns='requisite_id')
            )
        )
    )
    .add_stage(
        PipelineStage(
            name='select-data',
            stage_type=StageType.SELECTING,
        )
        .add_step(
            PipelineStep(
            name='select-requisite-data',
            function=PipelineStep.select,
            columns=Config.REQUISITES_COLUMNS,
            )
        )
    )
    .add_stage(
        PipelineStage(
            name='validate-data',
            stage_type=StageType.VALIDATING,
        )
        .add_step(
            PipelineStep(
                name='validate-course-prerequisite-types',
                function=PipelineStep.validate,
                validator=ChoiceValidatorStrategy(column='course_prerequisite_type',
                                                  values=Config.VALID_COURSE_PREREQUISITE_TYPES
                                                  ),
            )
        )
        .add_step(
            PipelineStep(
                name='validate-minimum-required-number-of-courses',
                function=PipelineStep.validate,
                validator=RangeValidatorStrategy(column='minimum_required_number_of_courses',
                                                 min=Config.VALID_MINIMUM_REQUIRED_NUMBER_OF_COURSES_RANGE.start,
                                                 max=Config.VALID_MINIMUM_REQUIRED_NUMBER_OF_COURSES_RANGE.stop)
            )
        )
    )
    .add_stage(
        PipelineStage(
            name='store-data',
            stage_type=StageType.STORING
        )
        .add_step(
            PipelineStep(
                name='store-requisite-data',
                function=PipelineStep.save_data,
                output_file_location=FileStorageMixin.get_output_file_location(),
                output_file_name=Config.REQUISITES_OUTPUT_FILE_NAME,
                columns=Config.REQUISITES_COLUMNS,
                drop_duplicates=True
            )
        )
    )
    )
