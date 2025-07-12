import pandas as pd

from src.configurations import DatasetConfiguration
from src.patterns.builder.pipeline import Pipeline
from src.patterns.builder.stage import PipelineStage
from src.patterns.builder.step import PipelineStep
from src.patterns.strategy.validator import ChoiceValidatorStrategy, UUIDValidatorStrategy
from src.validator.models.enums import StageType


def offers_validator(df_curricula: pd.DataFrame, df_study_programs: pd.DataFrame) -> Pipeline:
    return (Pipeline(
        name='offers-validator-pipeline'
    )
    .add_stage(
        PipelineStage(
            name='load-data',
            stage_type=StageType.LOAD
        )
        .add_step(
            PipelineStep(
                name='load-offers-data',
                function=PipelineStep.read_data,
                configuration=DatasetConfiguration.OFFERS
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
                name='validate-offers-id',
                function=PipelineStep.validate,
                strategy=UUIDValidatorStrategy(column='offers_id')
            )
        )
        .add_step(
            PipelineStep(
                name='validate-study-program-id',
                function=PipelineStep.validate,
                strategy=ChoiceValidatorStrategy(column='study_program_id',
                                                  values=set(df_study_programs['study_program_id'].values.tolist())),
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
    )
