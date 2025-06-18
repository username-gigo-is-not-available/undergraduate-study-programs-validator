from src.config import Config
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
            stage_type=StageType.LOADING
        )
        .add_step(
            PipelineStep(
                name='load-study-program-data',
                function=PipelineStep.read_data,
                input_file_location=PipelineStep.get_input_file_location(),
                input_file_name=Config.STUDY_PROGRAMS_INPUT_FILE_NAME,
                column_order=Config.STUDY_PROGRAMS_COLUMN_ORDER,
            )
        )
    ).add_stage(
        PipelineStage(
            name='validate-data',
            stage_type=StageType.VALIDATING
        )
        .add_step(
            PipelineStep(
                name='validate-study-program-id',
                function=PipelineStep.validate,
                validator=UUIDValidatorStrategy(column='study_program_id'),
            )
        )
        .add_step(
            PipelineStep(
                name='validate-study-program-code',
                function=PipelineStep.validate,
                validator=RegexValidatorStrategy(column='study_program_code', pattern=Config.STUDY_PROGRAM_CODE_REGEX),
            )
        )
        .add_step(
            PipelineStep(
                name='validate-study-program-url',
                function=PipelineStep.validate,
                validator=UrlValidatorStrategy(column='study_program_url'),
            )
        )
        .add_step(
            PipelineStep(
                name='validate-study-program-duration',
                function=PipelineStep.validate,
                validator=ChoiceValidatorStrategy(column='study_program_duration', values={2, 3, 4}),
            )
        )
    ).add_stage(
        PipelineStage(
            name='store-data',
            stage_type=StageType.STORING
        ).add_step(
            PipelineStep(
                name='store-study-program-data',
                function=PipelineStep.save_data,
                output_file_location=PipelineStep.get_output_file_location(),
                output_file_name=Config.STUDY_PROGRAMS_OUTPUT_FILE_NAME,
                column_order=Config.STUDY_PROGRAMS_COLUMN_ORDER,
            )
        )
    )
    )
