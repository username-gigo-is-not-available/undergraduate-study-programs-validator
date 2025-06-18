import pandas as pd

from src.config import Config
from src.patterns.builder.pipeline import Pipeline
from src.patterns.builder.stage import PipelineStage
from src.patterns.builder.step import PipelineStep
from src.patterns.strategy.filter import OrFilteringStrategy, NotEqualFilteringStrategy, NotNullFilteringStrategy, \
    GroupExistsFilteringStrategy, GroupHasAtLeastNMembersFilteringStrategy
from src.validator.models.enums import StageType, CoursePrerequisiteType


def offers_validator(df_requires: pd.DataFrame) -> Pipeline:
    def invalidate_prerequisites_stages(df_requires: pd.DataFrame) -> list[PipelineStage]:
        return [
            PipelineStage(
                name='merge-data',
                stage_type=StageType.MERGING
            ).add_step(
                PipelineStep(
                    name='merge-with-requires-data',
                    function=PipelineStep.merge,
                    merge_df=df_requires,
                    on='course_id',
                    how='left'
                )
            ).add_step(
                PipelineStep(
                    name='map-with-offers-data',
                    function=PipelineStep.self_merge,
                    left_on=['study_program_id', 'course_prerequisite_id'],
                    right_on=['study_program_id', 'course_id'],
                    columns=['study_program_id', 'course_id'],
                    suffixes=('_parent', '_child'),
                    how='left'
                )
            ),
            PipelineStage(
                name='filter-data',
                stage_type=StageType.FILTERING
            ).add_step(
                PipelineStep(
                    name='filter-one-type',
                    function=PipelineStep.filter,
                    filter=OrFilteringStrategy(
                        left=NotEqualFilteringStrategy(
                            column='course_prerequisite_type',
                            value=CoursePrerequisiteType.ONE
                        ),
                        right=NotNullFilteringStrategy(column='course_id_child')
                    )
                )
            ).add_step(
                PipelineStep(
                    name='filter-any-type',
                    function=PipelineStep.filter,
                    filter=OrFilteringStrategy(
                        left=NotEqualFilteringStrategy(
                            column='course_prerequisite_type',
                            value=CoursePrerequisiteType.ANY
                        ),
                        right=GroupExistsFilteringStrategy(
                            group_by_columns=['study_program_id', 'course_id_parent'],
                            evaluated_columns='course_id_child'
                        )
                    )
                )
            ).add_step(
                PipelineStep(
                    name='filter-total-type',
                    function=PipelineStep.filter,
                    filter=OrFilteringStrategy(
                        left=NotEqualFilteringStrategy(
                            column='course_prerequisite_type',
                            value=CoursePrerequisiteType.TOTAL
                        ),
                        right=GroupHasAtLeastNMembersFilteringStrategy(
                            group_by_columns=['study_program_id', 'course_id_parent'],
                            evaluated_columns='course_id_child',
                            threshold_columns='minimum_required_number_of_courses'
                        )
                    )
                )
            ),
            PipelineStage(
                name='rename-data',
                stage_type=StageType.RENAMING
            ).add_step(
                PipelineStep(
                    name='rename-parent-to-course',
                    function=PipelineStep.rename,
                    columns={'course_id_parent': 'course_id'}
                )
            ),
            PipelineStage(
                name='select-data',
                stage_type=StageType.SELECTING
            ).add_step(
                PipelineStep(
                    name='select-final-columns',
                    function=PipelineStep.select,
                    columns=Config.OFFERS_COLUMN_ORDER,
                    drop_duplicates=True
                )
            )
        ]

    pipeline: Pipeline = Pipeline(name='offers-validator-pipeline')
    pipeline.add_stage(
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
                column_order=Config.OFFERS_COLUMN_ORDER,
            )
        )
    )
    # Recursively invalidate prerequisites (max_depth = 2)
    for stage in invalidate_prerequisites_stages(df_requires):
        pipeline.add_stage(stage)

    for stage in invalidate_prerequisites_stages(df_requires):
        pipeline.add_stage(stage)

    pipeline.add_stage(
        PipelineStage(
            name='store-data',
            stage_type=StageType.STORING
        )
        .add_step(
            PipelineStep(
                name='store-offers-data',
                function=PipelineStep.save_data,
                output_file_location=PipelineStep.get_output_file_location(),
                output_file_name=Config.OFFERS_OUTPUT_FILE_NAME,
                column_order=Config.OFFERS_COLUMN_ORDER,

            )
        )
    )
    return pipeline
