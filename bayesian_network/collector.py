import itertools
from typing import List

import pandas as pd

from .connect import ConnectInfo, ConnectChecker


class DisconnectInfoCollector:
    def __init__(self, n_dim: int, connect_df: pd.DataFrame, connect_checker: ConnectChecker):
        self._n_dim = n_dim
        self._connect_df = connect_df
        self._df_columns = connect_df.columns.to_numpy()
        self._connect_checker = connect_checker
        self._disconnect_infos: List[ConnectInfo] = []

    @staticmethod
    def _get_combinations(elements):
        combinations = []
        for parsed_elements in itertools.combinations(elements, 2):
            remaining_elements = [ele for ele in elements if ele not in parsed_elements]
            combinations.append((*parsed_elements, remaining_elements))
        return combinations

    def _collect_if_disconnect(self, col1: str, col2: str, cond_cols: List[str] = []):
        if not self._connect_df.loc[col1, col2]:
            return
        info = self._connect_checker.check(col1, col2, cond_cols=cond_cols)
        print(info)
        if not info.is_connect:
            self._disconnect_infos.append(info)

    def _collect_disconnect_infos_recursive(self, current_cols: List[str], start: int):        
        if len(current_cols) == self._n_dim + 2:
            combinations = self._get_combinations(current_cols)
            for col1, col2, cond_cols in combinations:
                self._collect_if_disconnect(col1=col1, col2=col2, cond_cols=cond_cols)
            return
        
        for i in range(start, len(self._df_columns)):
            next_cols = [*current_cols, self._df_columns[i]]
            self._collect_disconnect_infos_recursive(current_cols=next_cols, start=i+1)

    def run(self):        
        self._collect_disconnect_infos_recursive(current_cols=[], start=0)
