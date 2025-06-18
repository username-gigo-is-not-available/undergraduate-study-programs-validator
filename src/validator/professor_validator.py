from src.config import Config
from src.patterns.builder.pipeline import Pipeline
from src.patterns.builder.stage import PipelineStage
from src.patterns.builder.step import PipelineStep
from src.patterns.strategy.validator import UUIDValidatorStrategy
from src.validator.models.enums import StageType


def professor_validator() -> Pipeline:
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
                name='load-professor-data',
                function=PipelineStep.read_data,
                input_file_location=PipelineStep.get_input_file_location(),
                input_file_name=Config.PROFESSORS_INPUT_FILE_NAME,
                column_order=Config.PROFESSORS_COLUMN_ORDER,
            )
        )
    ).add_stage(
        PipelineStage(
            name='validate-data',
            stage_type=StageType.VALIDATING
        )
        .add_step(
            PipelineStep(
                name='validate-professor-id',
                function=PipelineStep.validate,
                validator=UUIDValidatorStrategy(column='professor_id')
            )
        )
    ).add_stage(
        PipelineStage(
            name='store-data',
            stage_type=StageType.STORING
        ).add_step(
            PipelineStep(
                name='store-professor-data',
                function=PipelineStep.save_data,
                output_file_location=PipelineStep.get_output_file_location(),
                output_file_name=Config.PROFESSORS_OUTPUT_FILE_NAME,
                column_order=Config.PROFESSORS_COLUMN_ORDER,
            )
        )
    )
    )
