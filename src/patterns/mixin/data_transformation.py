from functools import wraps
from typing import Any, Literal

import pandas as pd

from src.patterns.strategy.filter import FilteringStrategy
from src.patterns.strategy.validator import ValidatorStrategy


class DataTransformationMixin:

    @staticmethod
    def _to_list(value: str | list[str]) -> list[str]:
        if value is not None:
            return [value] if isinstance(value, str) else value
        return []

    @staticmethod
    def _normalize_column_args(**kwargs) -> dict[str, Any]:
        for key in ['input_columns', 'output_columns', 'truth_columns', 'on']:
            if key in kwargs:
                kwargs[key] = DataTransformationMixin._to_list(kwargs.get(key))
        return kwargs

    @staticmethod
    def normalize_column_args(func: callable) -> callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> pd.DataFrame:
            kwargs = DataTransformationMixin._normalize_column_args(**kwargs)
            return func(*args, **kwargs)

        return wrapper

    def validate(self, df: pd.DataFrame,
                 validator: ValidatorStrategy,
                 ) -> pd.DataFrame:
        return validator.validate(df)

    def filter(self, df: pd.DataFrame,
               filter: FilteringStrategy,
               ) -> pd.DataFrame:
        return filter.filter(df)

    @normalize_column_args
    def select(self, df: pd.DataFrame,
               columns: str | list[str],
               drop_duplicates: bool = False):
        df: pd.DataFrame = df[columns]
        if drop_duplicates:
            df: pd.DataFrame = df.drop_duplicates()
        return df

    def rename(self, df: pd.DataFrame,
               columns: dict[str, str]
               ) -> pd.DataFrame:
        return df.rename(columns=columns)

    @normalize_column_args
    def self_merge(self, df: pd.DataFrame,
                   left_on: str | list[str],
                   right_on: str | list[str],
                   columns: str | list[str],
                   suffixes: tuple[str, str] = ('_x', '_y'),
                   how: Literal["left", "right", "inner", "outer", "cross"] = "inner"):
        lookup: pd.DataFrame = pd.DataFrame(df[columns]).drop_duplicates()
        return pd.merge(df, lookup, left_on=left_on, right_on=right_on, how=how, suffixes=suffixes)

    @normalize_column_args
    def merge(self, df: pd.DataFrame,
              merge_df: pd.DataFrame,
              on: str | list[str] = None,
              left_on: str | list[str] = None,
              right_on: str | list[str] = None,
              how: Literal["left", "right", "inner", "outer", "cross"] = "inner") -> pd.DataFrame:
        if left_on and right_on:
            return pd.merge(df, merge_df, left_on=left_on, right_on=right_on, how=how)
        elif on:
            return pd.merge(df, merge_df, on=on, how=how)
        else:
            raise AttributeError("You must specify either `on` or `left_on` or `right_on`")
