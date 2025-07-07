import pandas as pd

from src.patterns.strategy.validator import ValidatorStrategy


class DataValidationMixin:

    def validate(self, df: pd.DataFrame,
                 strategy: ValidatorStrategy,
                 ) -> pd.DataFrame:
        return strategy.validate(df)
