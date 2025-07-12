from src.configurations import DatasetConfiguration, ApplicationConfiguration
from src.patterns.builder.pipeline import Pipeline
from src.patterns.builder.stage import PipelineStage
from src.patterns.builder.step import PipelineStep
from src.patterns.strategy.validator import ChoiceValidatorStrategy, RangeValidatorStrategy, UUIDValidatorStrategy
from src.validator.models.enums import StageType


def curriculum_validator() -> Pipeline:
    return (
        Pipeline(name='curriculum-validator-pipeline')
        .add_stage(
            PipelineStage(
                name='load-data',
                stage_type=StageType.LOAD
            )
            .add_step(
                PipelineStep(
                    name='load-curricula-data',
                    function=PipelineStep.read_data,
                    configuration=DatasetConfiguration.CURRICULA
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
                    name='validate-curriculum-id',
                    function=PipelineStep.validate,
                    strategy=UUIDValidatorStrategy(column='curriculum_id')
                )
            )
            .add_step(
                PipelineStep(
                    name='validate-course-type',
                    function=PipelineStep.validate,
                    strategy=ChoiceValidatorStrategy(column='course_type',
                                                     values=ApplicationConfiguration.VALID_COURSE_TYPES)
                )
            )
            .add_step(
                PipelineStep(
                    name='validate-course-semester-season',
                    function=PipelineStep.validate,
                    strategy=ChoiceValidatorStrategy(column='course_semester_season',
                                                     values=ApplicationConfiguration.VALID_COURSE_SEMESTER_SEASONS)
                )
            )
            .add_step(
                PipelineStep(
                    name='validate-course-academic-year',
                    function=PipelineStep.validate,
                    strategy=RangeValidatorStrategy(column='course_academic_year',
                                                    min=ApplicationConfiguration.VALID_COURSE_ACADEMIC_YEARS_RANGE.start,
                                                    max=ApplicationConfiguration.VALID_COURSE_ACADEMIC_YEARS_RANGE.stop)
                )
            )
            .add_step(
                PipelineStep(
                    name='validate-course-semester',
                    function=PipelineStep.validate,
                    strategy=RangeValidatorStrategy(column='course_semester',
                                                    min=ApplicationConfiguration.VALID_COURSE_SEMESTERS_RANGE.start,
                                                    max=ApplicationConfiguration.VALID_COURSE_SEMESTERS_RANGE.stop)
                )
            )
        )
    )
