from src.configurations import DatasetConfiguration, ApplicationConfiguration
from src.patterns.builder.pipeline import Pipeline
from src.patterns.builder.stage import PipelineStage
from src.patterns.builder.step import PipelineStep
from src.patterns.strategy.validator import UrlValidatorStrategy, RegexValidatorStrategy, UUIDValidatorStrategy, \
    ChoiceValidatorStrategy
from src.validator.models.enums import StageType


def study_program_validator():
    return (Pipeline(
        name='study-program-validator-pipeline'
    )
    .add_stage(
        PipelineStage(
            name='load-data',
            stage_type=StageType.LOAD
        )
        .add_step(
            PipelineStep(
                name='load-study-program-data',
                function=PipelineStep.read_data,
                configuration=DatasetConfiguration.STUDY_PROGRAMS
            )
        )
    )
    .add_stage(
        PipelineStage(
            name='validate-data',
            stage_type=StageType.VALIDATE
        )
        .add_step(
            PipelineStep(
                name='validate-study-program-id',
                function=PipelineStep.validate,
                strategy=UUIDValidatorStrategy(column='study_program_id'),
            )
        )
        .add_step(
            PipelineStep(
                name='validate-study-program-code',
                function=PipelineStep.validate,
                strategy=RegexValidatorStrategy(column='study_program_code',
                                                pattern=ApplicationConfiguration.VALID_STUDY_PROGRAM_CODE_REGEX),
            )
        )
        .add_step(
            PipelineStep(
                name='validate-study-program-url',
                function=PipelineStep.validate,
                strategy=UrlValidatorStrategy(column='study_program_url'),
            )
        )
        .add_step(
            PipelineStep(
                name='validate-study-program-duration',
                function=PipelineStep.validate,
                strategy=ChoiceValidatorStrategy(column='study_program_duration',
                                                 values=ApplicationConfiguration.VALID_STUDY_PROGRAM_DURATIONS),
            )
        )
    )
    )
