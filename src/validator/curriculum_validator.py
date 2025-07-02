import pandas as pd

from src.config import Config
from src.patterns.builder.pipeline import Pipeline
from src.patterns.builder.stage import PipelineStage
from src.patterns.builder.step import PipelineStep
from src.patterns.strategy.filter import OrFilteringStrategy, NotEqualFilteringStrategy, NotNullFilteringStrategy, \
    GroupExistsFilteringStrategy, GroupHasAtLeastNMembersFilteringStrategy
from src.validator.models.enums import StageType, CoursePrerequisiteType


def curriculum_validator(df_requisites: pd.DataFrame, df_offers: pd.DataFrame, df_includes: pd.DataFrame,
                         df_prerequisites: pd.DataFrame, df_postrequisites: pd.DataFrame) -> Pipeline:
    def invalidate_requisites_stages(df_requisites: pd.DataFrame,
                                     df_offers: pd.DataFrame,
                                     df_includes: pd.DataFrame,
                                     df_prerequisites: pd.DataFrame,
                                     df_postrequisites: pd.DataFrame) -> list[PipelineStage]:
        return [
            PipelineStage(
                name='merge-data',
                stage_type=StageType.MERGING
            )
            .add_step(
                PipelineStep(
                    name='merge-with-offers-data',
                    function=PipelineStep.merge,
                    merge_df=df_offers,
                    on='curriculum_id',
                )
            )
            .add_step(
                PipelineStep(
                    name='merge-with-includes-data',
                    function=PipelineStep.merge,
                    merge_df=df_includes,
                    on='curriculum_id',
                )
            )
            .add_step(
                PipelineStep(
                    name='merge-with-postrequisites-data',
                    function=PipelineStep.merge,
                    merge_df=df_postrequisites,
                    on='course_id',
                    how='left'
                )
            )
            .add_step(
                PipelineStep(
                    name='merge-with-requisite-data',
                    function=PipelineStep.merge,
                    merge_df=df_requisites,
                    on='requisite_id',
                    how='left'
                )
            )
            .add_step(
                PipelineStep(
                    name='merge-with-prerequisite-data',
                    function=PipelineStep.merge,
                    merge_df=df_prerequisites,
                    on='requisite_id',
                    how='left'
                )
            )
            .add_step(
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
                    name='rename-parent-course-id',
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
                    columns=Config.CURRICULA_COLUMNS,
                    drop_duplicates=True
                )
            )
        ]

    pipeline: Pipeline = Pipeline(name='curriculum-validator-pipeline')
    pipeline.add_stage(
        PipelineStage(
            name='load-data',
            stage_type=StageType.LOADING
        )
        .add_step(
            PipelineStep(
                name='load-curricula-data',
                function=PipelineStep.read_data,
                input_file_location=PipelineStep.get_input_file_location(),
                input_file_name=Config.CURRICULA_INPUT_FILE_NAME,
                columns=Config.CURRICULA_COLUMNS,
                drop_duplicates=True
            )
        )
    )
    # Recursively invalidate prerequisites (max_depth = 2)
    for stage in invalidate_requisites_stages(df_requisites, df_offers, df_includes, df_prerequisites,
                                              df_postrequisites):
        pipeline.add_stage(stage)

    for stage in invalidate_requisites_stages(df_requisites, df_offers, df_includes, df_prerequisites,
                                              df_postrequisites):
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
                output_file_name=Config.CURRICULA_OUTPUT_FILE_NAME,
                columns=Config.CURRICULA_COLUMNS,
                drop_duplicates=True
            )
        )
    )
    return pipeline
