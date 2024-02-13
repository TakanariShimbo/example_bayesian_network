import itertools
from typing import List

import pandas as pd

from .connection import ConnectionInfo, ConnectionChecker


class DisconnectionInfosCollector:
    def __init__(self, n_dim: int, connection_df: pd.DataFrame, connection_checker: ConnectionChecker):
        self._n_dim = n_dim
        self._connection_df = connection_df
        self._column_names = connection_df.columns.to_list()
        self._connection_checker = connection_checker
        self._disconnection_infos: List[ConnectionInfo] = []

    @staticmethod
    def _get_combinations(elements):
        combinations = []
        for parsed_elements in itertools.combinations(elements, 2):
            remaining_elements = [e for e in elements if e not in parsed_elements]
            combinations.append((*parsed_elements, remaining_elements))
        return combinations

    def _collect_if_disconnecting(self, column1: str, column2: str, condition_columns: List[str] = []):
        if not self._connection_df.loc[column1, column2]:
            return
        connection_info = self._connection_checker.check(column1=column1, column2=column2, condition_columns=condition_columns)
        print(connection_info)
        if not connection_info.is_connecting:
            self._disconnection_infos.append(connection_info)

    def _collect_disconnection_infos_recursive(self, current_columns: List[str], start: int):
        if len(current_columns) == self._n_dim + 2:
            combinations = self._get_combinations(current_columns)
            for column1, column2, condition_columns in combinations:
                self._collect_if_disconnecting(column1=column1, column2=column2, condition_columns=condition_columns)
            return

        for i in range(start, len(self._column_names)):
            next_columns = [*current_columns, self._column_names[i]]
            self._collect_disconnection_infos_recursive(current_columns=next_columns, start=i + 1)

    def collect(self):
        self._collect_disconnection_infos_recursive(current_columns=[], start=0)
