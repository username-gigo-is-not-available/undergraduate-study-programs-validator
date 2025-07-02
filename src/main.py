import logging
import time

import pandas as pd

from src.config import Config
from src.patterns.builder.step import PipelineStep
from src.patterns.mixin.file_storage import FileStorageMixin
from src.validator.course_validator import course_validator
from src.validator.curriculum_validator import curriculum_validator
from src.validator.includes_validator import includes_validator
from src.validator.offers_validator import offers_validator
from src.validator.postrequisite_validator import postrequisite_validator
from src.validator.prerequisite_validator import prerequisite_validator
from src.validator.professor_validator import professor_validator
from src.validator.requisite_validator import requisite_validator
from src.validator.study_program_validator import study_program_validator
from src.validator.teaches_validator import teaches_validator

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    logging.info("Starting...")
    start: float = time.perf_counter()
    df_courses: pd.DataFrame = course_validator().build().run()
    df_professors: pd.DataFrame = professor_validator().build().run()
    df_study_programs: pd.DataFrame = study_program_validator().build().run()
    teaches_validator(df_courses, df_professors).build().run()
    df_prerequisites: pd.DataFrame = FileStorageMixin().read_data(PipelineStep.get_input_file_location(),
                                                                  Config.PREREQUISITES_INPUT_FILE_NAME,
                                                                  Config.PREREQUISITES_COLUMNS)
    df_postrequisites: pd.DataFrame = FileStorageMixin().read_data(PipelineStep.get_input_file_location(),
                                                                   Config.POSTREQUISITES_INPUT_FILE_NAME,
                                                                   Config.POSTREQUISITES_COLUMNS)
    df_includes: pd.DataFrame = FileStorageMixin().read_data(PipelineStep.get_input_file_location(),
                                                             Config.INCLUDES_INPUT_FILE_NAME, Config.INCLUDES_COLUMNS)
    df_offers: pd.DataFrame = FileStorageMixin().read_data(PipelineStep.get_input_file_location(),
                                                           Config.OFFERS_INPUT_FILE_NAME, Config.OFFERS_COLUMNS)
    df_requisites: pd.DataFrame = requisite_validator(df_prerequisites, df_offers, df_includes).build().run()
    df_curricula: pd.DataFrame = curriculum_validator(df_requisites, df_offers, df_includes, df_prerequisites,
                                                      df_postrequisites).build().run()
    includes_validator(df_curricula, df_courses).build().run()
    offers_validator(df_curricula, df_study_programs).build().run()
    prerequisite_validator(df_requisites, df_courses).build().run()
    postrequisite_validator(df_requisites, df_courses).build().run()
    logging.info(f"Time taken: {time.perf_counter() - start:.2f} seconds")
