import pandas as pd

from src.configurations import DatasetConfiguration
from src.patterns.builder.pipeline import Pipeline
from src.patterns.builder.stage import PipelineStage
from src.patterns.builder.step import PipelineStep
from src.patterns.strategy.validator import ChoiceValidatorStrategy, UUIDValidatorStrategy
from src.validator.models.enums import StageType


def satisfies_validator(df_requisites: pd.DataFrame, df_courses: pd.DataFrame) -> Pipeline:
    return (Pipeline(
        name='satisfies-validator-pipeline'
    )
    .add_stage(
        PipelineStage(
            name='load-data',
            stage_type=StageType.LOAD
        )
        .add_step(
            PipelineStep(
                name='load-satisfies-data',
                function=PipelineStep.read_data,
                configuration=DatasetConfiguration.SATISFIES
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
                name='validate-satisfies-id',
                function=PipelineStep.validate,
                strategy=UUIDValidatorStrategy(column='satisfies_id')
            )
        )
        .add_step(
            PipelineStep(
                name='validate-course-id',
                function=PipelineStep.validate,
                strategy=ChoiceValidatorStrategy(column='prerequisite_course_id',
                                                  values=set(df_courses['course_id'].values.tolist())),
            )
        )
        .add_step(
            PipelineStep(
                name='validate-requisite-id',
                function=PipelineStep.validate,
                strategy=ChoiceValidatorStrategy(column='requisite_id',
                                                  values=set(df_requisites['requisite_id'].values.tolist())),
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
                name='store-satisfies-data',
                function=PipelineStep.save_data,
                configuration=DatasetConfiguration.SATISFIES
            )
        )
    )
    )
