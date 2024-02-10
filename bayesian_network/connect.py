from typing import List

import pandas as pd

from .chi import chi_square_test


class ConnectInfo:
    def __init__(self, p_val: float, col1: str, col2: str, cond_cols: List[str] = [], p_threshold: float = 0.05):
        self.is_connect = p_val < p_threshold
        self.p_val = p_val
        self.col1 = col1
        self.col2 = col2
        self.cond_cols = cond_cols

    def __str__(self) -> str:
        return f"{self.col1} , {self.col2} | {self.cond_cols} -> {self.is_connect} [{self.p_val:.2f}]"

    def __repr__(self) -> str:
        return f"{self.col1} , {self.col2} | {self.cond_cols} -> {self.is_connect} [{self.p_val:.2f}]"


class ConnectChecker:
    def __init__(self, bin_df: pd.DataFrame, p_threshold: float = 0.05):
        self._bin_df = bin_df
        self._p_threshold = p_threshold

    def check(self, col1: str, col2: str, cond_cols: List[str] = []) -> ConnectInfo:
        p_val = chi_square_test(col1=col1, col2=col2, cond_cols=cond_cols, bin_df=self._bin_df)
        connect_info = ConnectInfo(p_val, col1, col2, cond_cols=cond_cols, p_threshold=self._p_threshold)
        return connect_info
