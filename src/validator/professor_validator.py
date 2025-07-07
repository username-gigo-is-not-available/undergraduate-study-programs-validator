from src.configurations import DatasetConfiguration
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
            stage_type=StageType.LOAD
        )
        .add_step(
            PipelineStep(
                name='load-professor-data',
                function=PipelineStep.read_data,
                configuration=DatasetConfiguration.PROFESSORS,
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
                name='validate-professor-id',
                function=PipelineStep.validate,
                strategy=UUIDValidatorStrategy(column='professor_id')
            )
        )
    )
    .add_stage(
        PipelineStage(
            name='store-data',
            stage_type=StageType.STORE
        ).add_step(
            PipelineStep(
                name='store-professor-data',
                function=PipelineStep.save_data,
                configuration=DatasetConfiguration.PROFESSORS,
            )
        )
    )
    )
