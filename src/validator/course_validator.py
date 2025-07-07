from src.configurations import DatasetConfiguration, ApplicationConfiguration
from src.patterns.builder.pipeline import Pipeline
from src.patterns.builder.stage import PipelineStage
from src.patterns.builder.step import PipelineStep
from src.patterns.strategy.validator import UrlValidatorStrategy, RegexValidatorStrategy, UUIDValidatorStrategy, \
    ChoiceValidatorStrategy
from src.validator.models.enums import StageType


def course_validator() -> Pipeline:
    return (Pipeline(
        name='course-validator-pipeline'
    )
    .add_stage(
        PipelineStage(
            name='load-data',
            stage_type=StageType.LOAD
        )
        .add_step(
            PipelineStep(
                name='load-course-data',
                function=PipelineStep.read_data,
                configuration=DatasetConfiguration.COURSES,
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
                name='validate-course-id',
                function=PipelineStep.validate,
                strategy=UUIDValidatorStrategy(column='course_id'),
            )
        )
        .add_step(
            PipelineStep(
                name='validate-course-code',
                function=PipelineStep.validate,
                strategy=RegexValidatorStrategy(column='course_code',
                                                pattern=ApplicationConfiguration.VALID_COURSE_CODE_REGEX)
            )
        )
        .add_step(
            PipelineStep(
                name='validate-course-url',
                function=PipelineStep.validate,
                strategy=UrlValidatorStrategy(column='course_url'),
            )
        )
        .add_step(
            PipelineStep(
                name='validate-course-level',
                function=PipelineStep.validate,
                strategy=ChoiceValidatorStrategy(column='course_level',
                                                 values=ApplicationConfiguration.VALID_COURSE_LEVELS)
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
                name='store-course-data',
                function=PipelineStep.save_data,
                configuration=DatasetConfiguration.COURSES,
            )
        )
    )
    )
