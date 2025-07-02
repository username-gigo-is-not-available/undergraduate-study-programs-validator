import pandas as pd

from src.config import Config
from src.patterns.builder.pipeline import Pipeline
from src.patterns.builder.stage import PipelineStage
from src.patterns.builder.step import PipelineStep
from src.patterns.mixin.file_storage import FileStorageMixin
from src.patterns.strategy.filter import NotNullFilteringStrategy
from src.patterns.strategy.validator import ChoiceValidatorStrategy
from src.validator.models.enums import StageType


def offers_validator(df_curricula: pd.DataFrame, df_study_programs: pd.DataFrame) -> Pipeline:
    return (Pipeline(
        name='offers-validator-pipeline'
    )
    .add_stage(
        PipelineStage(
            name='load-data',
            stage_type=StageType.LOADING
        )
        .add_step(
            PipelineStep(
                name='load-offers-data',
                function=PipelineStep.read_data,
                input_file_location=PipelineStep.get_input_file_location(),
                input_file_name=Config.OFFERS_INPUT_FILE_NAME,
                columns=Config.OFFERS_COLUMNS,
                drop_duplicates=True
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
                name='merge-with-curricula-data',
                function=PipelineStep.merge,
                merge_df=df_curricula,
                how='left',
                on='curriculum_id',
            )
        )
    )
    .add_stage(
        PipelineStage(
            name='filter-data',
            stage_type=StageType.FILTERING
        )
        .add_step(
            PipelineStep(
                name='filter-out-invalid-curricula-data',
                function=PipelineStep.filter,
                filter=NotNullFilteringStrategy('course_semester')
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
                name='validate-study-program-id',
                function=PipelineStep.validate,
                validator=ChoiceValidatorStrategy(column='study_program_id',
                                                  values=set(df_study_programs['study_program_id'].values.tolist())),
            )
        )
        .add_step(
            PipelineStep(
                name='validate-curriculum-id',
                function=PipelineStep.validate,
                validator=ChoiceValidatorStrategy(column='curriculum_id',
                                                  values=set(df_curricula['curriculum_id'].values.tolist())),
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
                name='store-includes-data',
                function=PipelineStep.save_data,
                output_file_location=FileStorageMixin.get_output_file_location(),
                output_file_name=Config.OFFERS_OUTPUT_FILE_NAME,
                columns=Config.OFFERS_COLUMNS,
                drop_duplicates=True
            )
        )
    )
    )
