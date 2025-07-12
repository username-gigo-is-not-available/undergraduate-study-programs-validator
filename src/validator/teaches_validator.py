import pandas as pd

from src.configurations import DatasetConfiguration
from src.patterns.builder.pipeline import Pipeline
from src.patterns.builder.stage import PipelineStage
from src.patterns.builder.step import PipelineStep
from src.patterns.strategy.validator import ChoiceValidatorStrategy, UUIDValidatorStrategy
from src.validator.models.enums import StageType


def teaches_validator(df_courses: pd.DataFrame, df_professors: pd.DataFrame) -> Pipeline:
    return (Pipeline(
        name='teaches-validator-pipeline'
    )
    .add_stage(
        PipelineStage(
            name='load-data',
            stage_type=StageType.LOAD
        )
        .add_step(
            PipelineStep(
                name='load-teaches-data',
                function=PipelineStep.read_data,
                configuration=DatasetConfiguration.TEACHES,
            )
        )
    )
    .add_stage(
        PipelineStage(
            name='validate-data',
            stage_type=StageType.VALIDATE,
        )
        .add_step(
            PipelineStep(
                name='validate-teaches-id',
                function=PipelineStep.validate,
                strategy=UUIDValidatorStrategy(column='teaches_id')
            )
        )
        .add_step(
            PipelineStep(
                name='validate-professor-id',
                function=PipelineStep.validate,
                strategy=ChoiceValidatorStrategy(column='professor_id',
                                                 values=set(df_professors['professor_id'].values.tolist())),
            )
        )
        .add_step(
            PipelineStep(
                name='validate-course-id',
                function=PipelineStep.validate,
                strategy=ChoiceValidatorStrategy(column='course_id',
                                                 values=set(df_courses['course_id'].values.tolist())),
            )
        )
    )
    )
