import logging
import time

import pandas as pd

from src.validator.course_validator import course_validator
from src.validator.offers_validator import offers_validator
from src.validator.professor_validator import professor_validator
from src.validator.requires_validator import requires_validator
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
    df_requires: pd.DataFrame = requires_validator(df_courses).build().run()
    df_offers: pd.DataFrame = offers_validator(df_requires).build().run()

    logging.info(f"Time taken: {time.perf_counter() - start:.2f} seconds")

