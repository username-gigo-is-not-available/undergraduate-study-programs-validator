from src.config import Config
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
            stage_type=StageType.LOADING
        )
        .add_step(
            PipelineStep(
                name='load-course-data',
                function=PipelineStep.read_data,
                input_file_location=PipelineStep.get_input_file_location(),
                input_file_name=Config.COURSES_INPUT_FILE_NAME,
                columns=Config.COURSES_COLUMNS,
                drop_duplicates=True
            )
        )
    ).add_stage(
        PipelineStage(
            name='validate-data',
            stage_type=StageType.VALIDATING
        )
        .add_step(
            PipelineStep(
                name='validate-course-id',
                function=PipelineStep.validate,
                validator=UUIDValidatorStrategy(column='course_id'),
            )
        )
        .add_step(
            PipelineStep(
                name='validate-course-code',
                function=PipelineStep.validate,
                validator=RegexValidatorStrategy(column='course_code', pattern=Config.VALID_COURSE_CODE_REGEX)
            )
        )
        .add_step(
            PipelineStep(
                name='validate-course-url',
                function=PipelineStep.validate,
                validator=UrlValidatorStrategy(column='course_url'),
            )
        )
        .add_step(
            PipelineStep(
                name='validate-course-level',
                function=PipelineStep.validate,
                validator=ChoiceValidatorStrategy(column='course_level', values=Config.VALID_COURSE_LEVELS)
            )
        )
    ).add_stage(
        PipelineStage(
            name='store-data',
            stage_type=StageType.STORING
        ).add_step(
            PipelineStep(
                name='store-course-data',
                function=PipelineStep.save_data,
                output_file_location=PipelineStep.get_output_file_location(),
                output_file_name=Config.COURSES_OUTPUT_FILE_NAME,
                columns=Config.COURSES_COLUMNS,
                drop_duplicates=True
            )
        )
    )
    )
