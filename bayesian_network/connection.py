from typing import List

import pandas as pd

from .chi_square_test import chi_square_test


class ConnectionInfo:
    def __init__(self, p_value: float, column1: str, column2: str, condition_columns: List[str] = [], p_threshold: float = 0.05):
        self.is_connecting = p_value < p_threshold
        self.p_value = p_value
        self.column1 = column1
        self.column2 = column2
        self.condition_columns = condition_columns

    def __str__(self) -> str:
        return f"{self.column1} , {self.column2} | {self.condition_columns} -> {self.is_connecting} [{self.p_value:.2f}]"

    def __repr__(self) -> str:
        return f"{self.column1} , {self.column2} | {self.condition_columns} -> {self.is_connecting} [{self.p_value:.2f}]"


class ConnectionChecker:
    def __init__(self, bin_df: pd.DataFrame, p_threshold: float = 0.05):
        self._bin_df = bin_df
        self._p_threshold = p_threshold

    def check(self, column1: str, column2: str, condition_columns: List[str] = []) -> ConnectionInfo:
        p_value = chi_square_test(column1=column1, column2=column2, condition_columns=condition_columns, bin_df=self._bin_df)
        connection_info = ConnectionInfo(p_value, column1, column2, condition_columns=condition_columns, p_threshold=self._p_threshold)
        return connection_info
