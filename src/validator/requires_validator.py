import pandas as pd

from src.config import Config
from src.patterns.builder.pipeline import Pipeline
from src.patterns.builder.stage import PipelineStage
from src.patterns.builder.step import PipelineStep
from src.patterns.mixin.file_storage import FileStorageMixin
from src.patterns.strategy.filter import NotEqualFilteringStrategy
from src.patterns.strategy.validator import ChoiceValidatorStrategy
from src.validator.models.enums import StageType, CoursePrerequisiteType


def requires_validator(df_courses: pd.DataFrame) -> Pipeline:
    return (Pipeline(
        name='requires-validator-pipeline'
    )
    .add_stage(
        PipelineStage(
            name='load-data',
            stage_type=StageType.LOADING
        )
        .add_step(
            PipelineStep(
                name='load-requires-data',
                function=PipelineStep.read_data,
                input_file_location=PipelineStep.get_input_file_location(),
                input_file_name=Config.REQUIRES_INPUT_FILE_NAME,
                column_order=Config.REQUIRES_COLUMN_ORDER,
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
    ).add_stage(
        PipelineStage(
            name='validate-data',
            stage_type=StageType.VALIDATING,
        )
        .add_step(
            PipelineStep(
                name='validate-course-id',
                function=PipelineStep.validate,
                validator=ChoiceValidatorStrategy(column='course_id', values=set(df_courses['course_id'].values.tolist())),
            )
        )
        .add_step(
            PipelineStep(
                name='validate-course-prerequisite-id',
                function=PipelineStep.validate,
                validator=ChoiceValidatorStrategy(column='course_prerequisite_id', values=set(df_courses.course_id.values.tolist())),
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
                name='store-teaches-data',
                function=PipelineStep.save_data,
                output_file_location=FileStorageMixin.get_output_file_location(),
                output_file_name=Config.REQUIRES_OUTPUT_FILE_NAME,
                column_order=Config.REQUIRES_COLUMN_ORDER
            )
        )
    )
    )
