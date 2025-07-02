import re
from typing import Hashable

import pandas as pd
import validators


class ValidatorStrategy:
    def __init__(self, column: str):
        self.column = column

    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError("Subclasses must implement the validate method.")

    def check(self, df: pd.DataFrame, invalid_mask: pd.Series) -> pd.DataFrame:
        if invalid_mask.any():
            invalid_records = df[invalid_mask]
            raise ValueError(f"{self.__class__.__name__} validation failed for records: {invalid_records.values.tolist()}")
        return df

class RegexValidatorStrategy(ValidatorStrategy):
    def __init__(self, column: str, pattern: re.Pattern[str]):
        super().__init__(column)
        self.pattern = pattern

    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        invalid_mask = ~df[self.column].str.match(self.pattern, na=False)
        return self.check(df=df, invalid_mask=invalid_mask)


class UrlValidatorStrategy(ValidatorStrategy):

    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        def is_valid_url(url: str) -> bool:
            return validators.url(url) if pd.notnull(url) else False
        invalid_mask = ~df[self.column].apply(is_valid_url)
        return self.check(df=df, invalid_mask=invalid_mask)


class UUIDValidatorStrategy(ValidatorStrategy):

    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        def is_valid_uuid(uuid: str) -> bool:
            return validators.uuid(uuid) if pd.notnull(uuid) else False
        invalid_mask = ~df[self.column].apply(is_valid_uuid)
        return self.check(df=df, invalid_mask=invalid_mask)


class ChoiceValidatorStrategy(ValidatorStrategy):
    def __init__(self, column: str, values: set[Hashable]):
        super().__init__(column)
        self.values = values

    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        invalid_mask = ~df[self.column].isin(self.values)
        return self.check(df=df, invalid_mask=invalid_mask)

class RangeValidatorStrategy(ValidatorStrategy):
    def __init__(self, column: str, min: int, max: int):
        super().__init__(column)
        self.min = min
        self.max = max

    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        invalid_mask = ~df[self.column].between(self.min, self.max, inclusive='both')
        return self.check(df=df, invalid_mask=invalid_mask)
