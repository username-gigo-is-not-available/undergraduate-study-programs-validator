from functools import wraps
from typing import Any

import pandas as pd

from src.patterns.strategy.validator import ValidatorStrategy


class DataValidationMixin:

    @staticmethod
    def _to_list(value: str | list[str]) -> list[str]:
        if value is not None:
            return [value] if isinstance(value, str) else value
        return []

    @staticmethod
    def _normalize_column_args(**kwargs) -> dict[str, Any]:
        for key in ['input_columns', 'output_columns', 'truth_columns', 'on']:
            if key in kwargs:
                kwargs[key] = DataValidationMixin._to_list(kwargs.get(key))
        return kwargs

    @staticmethod
    def normalize_column_args(func: callable) -> callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> pd.DataFrame:
            kwargs = DataValidationMixin._normalize_column_args(**kwargs)
            return func(*args, **kwargs)

        return wrapper

    def validate(self, df: pd.DataFrame,
                 strategy: ValidatorStrategy,
                 ) -> pd.DataFrame:
        return strategy.validate(df)
