from src.configurations import DatasetConfiguration, ApplicationConfiguration
from src.patterns.builder.pipeline import Pipeline
from src.patterns.builder.stage import PipelineStage
from src.patterns.builder.step import PipelineStep
from src.patterns.strategy.validator import ChoiceValidatorStrategy, RangeValidatorStrategy, UUIDValidatorStrategy
from src.validator.models.enums import StageType


def requisite_validator() -> Pipeline:
    return (Pipeline(
        name='requisite-validator-pipeline'
    )
    .add_stage(
        PipelineStage(
            name='load-data',
            stage_type=StageType.LOAD
        )
        .add_step(
            PipelineStep(
                name='load-requisite-data',
                function=PipelineStep.read_data,
                configuration=DatasetConfiguration.REQUISITES

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
                name='validate-requisite-id',
                function=PipelineStep.validate,
                strategy=UUIDValidatorStrategy(column='requisite_id')
            )
        )
        .add_step(
            PipelineStep(
                name='validate-course-prerequisite-types',
                function=PipelineStep.validate,
                strategy=ChoiceValidatorStrategy(column='course_prerequisite_type',
                                                 values=ApplicationConfiguration.VALID_COURSE_PREREQUISITE_TYPES
                                                 )
            )
        )
        .add_step(
            PipelineStep(
                name='validate-minimum-required-number-of-courses',
                function=PipelineStep.validate,
                strategy=RangeValidatorStrategy(column='minimum_required_number_of_courses',
                                                min=ApplicationConfiguration.VALID_MINIMUM_REQUIRED_NUMBER_OF_COURSES_RANGE.start,
                                                max=ApplicationConfiguration.VALID_MINIMUM_REQUIRED_NUMBER_OF_COURSES_RANGE.stop)
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
                name='store-requisite-data',
                function=PipelineStep.save_data,
                configuration=DatasetConfiguration.REQUISITES
            )
        )
    )
    )
