import pandas as pd

from src.config import Config
from src.patterns.builder.pipeline import Pipeline
from src.patterns.builder.stage import PipelineStage
from src.patterns.builder.step import PipelineStep
from src.patterns.mixin.file_storage import FileStorageMixin
from src.patterns.strategy.filter import NotNullFilteringStrategy
from src.patterns.strategy.validator import ChoiceValidatorStrategy
from src.validator.models.enums import StageType


def prerequisite_validator(df_requisites: pd.DataFrame, df_courses: pd.DataFrame) -> Pipeline:
    return (Pipeline(
        name='prerequisite-validator-pipeline'
    )
    .add_stage(
        PipelineStage(
            name='load-data',
            stage_type=StageType.LOADING
        )
        .add_step(
            PipelineStep(
                name='load-prerequisite-data',
                function=PipelineStep.read_data,
                input_file_location=PipelineStep.get_input_file_location(),
                input_file_name=Config.PREREQUISITES_INPUT_FILE_NAME,
                columns=Config.PREREQUISITES_COLUMNS,
                drop_duplicates=True
            )
        )
    )
    .add_stage(
        PipelineStage(
            name='filter-data',
            stage_type=StageType.FILTERING,
        ).add_step(
            PipelineStep(
                name='filter-out-null-prerequisites',
                function=PipelineStep.filter,
                filter=NotNullFilteringStrategy(column='prerequisite_id'),
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
                validator=ChoiceValidatorStrategy(column='course_prerequisite_id',
                                                  values=set(df_courses['course_id'].values.tolist())),
            )
        )
        .add_step(
            PipelineStep(
                name='validate-requisite-id',
                function=PipelineStep.validate,
                validator=ChoiceValidatorStrategy(column='requisite_id',
                                                  values=set(df_requisites['requisite_id'].values.tolist())),
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
                name='store-prerequisite-data',
                function=PipelineStep.save_data,
                output_file_location=FileStorageMixin.get_output_file_location(),
                output_file_name=Config.PREREQUISITES_OUTPUT_FILE_NAME,
                columns=Config.PREREQUISITES_COLUMNS,
                drop_duplicates=True
            )
        )
    )
    )
