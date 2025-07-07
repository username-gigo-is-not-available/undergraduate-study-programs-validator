import pandas as pd

from src.configurations import DatasetConfiguration
from src.patterns.builder.pipeline import Pipeline
from src.patterns.builder.stage import PipelineStage
from src.patterns.builder.step import PipelineStep
from src.patterns.strategy.validator import ChoiceValidatorStrategy, UUIDValidatorStrategy
from src.validator.models.enums import StageType


def includes_validator(df_curricula: pd.DataFrame, df_courses: pd.DataFrame) -> Pipeline:
    return (Pipeline(
        name='includes-validator-pipeline'
    )
    .add_stage(
        PipelineStage(
            name='load-data',
            stage_type=StageType.LOAD
        )
        .add_step(
            PipelineStep(
                name='load-includes-data',
                function=PipelineStep.read_data,
                configuration=DatasetConfiguration.INCLUDES
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
                name='validate-includes-id',
                function=PipelineStep.validate,
                strategy=UUIDValidatorStrategy(column='includes_id')
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
        .add_step(
            PipelineStep(
                name='validate-curriculum-id',
                function=PipelineStep.validate,
                strategy=ChoiceValidatorStrategy(column='curriculum_id',
                                                  values=set(df_curricula['curriculum_id'].values.tolist())),
            )
        )
    )
    .add_stage(
        PipelineStage(
            name='store-data',
            stage_type=StageType.STORE
        )
        .add_step(
            PipelineStep(
                name='store-includes-data',
                function=PipelineStep.save_data,
                configuration=DatasetConfiguration.INCLUDES
            )
        )
    )
    )
