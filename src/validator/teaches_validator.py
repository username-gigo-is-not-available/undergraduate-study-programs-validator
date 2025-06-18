import pandas as pd

from src.config import Config
from src.patterns.builder.pipeline import Pipeline
from src.patterns.builder.stage import PipelineStage
from src.patterns.builder.step import PipelineStep
from src.patterns.strategy.filter import NotNullFilteringStrategy
from src.patterns.strategy.validator import ChoiceValidatorStrategy
from src.validator.models.enums import StageType


def teaches_validator(df_courses: pd.DataFrame, df_professors: pd.DataFrame) -> Pipeline:
    return (Pipeline(
        name='teaches-validator-pipeline'
    )
    .add_stage(
        PipelineStage(
            name='load-data',
            stage_type=StageType.LOADING
        )
        .add_step(
            PipelineStep(
                name='load-teaches-data',
                function=PipelineStep.read_data,
                input_file_location=PipelineStep.get_input_file_location(),
                input_file_name=Config.TEACHES_INPUT_FILE_NAME,
                column_order=Config.TEACHES_COLUMN_ORDER,
            )
        )
    )
    .add_stage(
        PipelineStage(
            name='filter-data',
            stage_type=StageType.FILTERING,
        ).add_step(
            PipelineStep(
                name='filter-out-null-professor-ids',
                function=PipelineStep.filter,
                filter=NotNullFilteringStrategy(column='professor_id')
            )
        )
    ).add_stage(
        PipelineStage(
            name='validate-data',
            stage_type=StageType.VALIDATING,
        )
        .add_step(
            PipelineStep(
                name='validate-professor-id',
                function=PipelineStep.validate,
                validator=ChoiceValidatorStrategy(column='professor_id', values=set(df_professors['professor_id'].values.tolist())),
            )
        )
        .add_step(
            PipelineStep(
                name='validate-course-id',
                function=PipelineStep.validate,
                validator=ChoiceValidatorStrategy(column='course_id', values=set(df_courses['course_id'].values.tolist())),
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
                output_file_location=PipelineStep.get_output_file_location(),
                output_file_name=Config.TEACHES_OUTPUT_FILE_NAME,
                column_order=Config.TEACHES_COLUMN_ORDER
            )
        )
    )
    )
