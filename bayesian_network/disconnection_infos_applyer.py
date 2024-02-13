import itertools
from typing import List

import numpy as np
import pandas as pd

from .connection import ConnectionInfo


class DisconnectionInfosApplyer:
    def __init__(self, n_dim: int, connection_df: pd.DataFrame, disconnection_infos: List[ConnectionInfo]):
        self._n_dim = n_dim
        self._connection_df = connection_df
        self._disconnection_infos = disconnection_infos

    @staticmethod
    def _generate_xxxxxs(n_dim: int):
        permutations = list(itertools.permutations(np.arange(n_dim) + 2))
        xxxxxs = []
        for xxxxx_list in permutations:
            xxx = ''.join(map(str, xxxxx_list))
            xxxxx = f"0{xxx}1"
            xxxxxs.append(xxxxx)
        return xxxxxs

    @staticmethod
    def _check_ab_is_connecting(index_pair: List[int], columns: List[str], connection_df: pd.DataFrame) -> bool:
        index_pair.sort()
        index_a, index_b = index_pair
        column_a = columns[index_a]
        column_b = columns[index_b]
        is_ab_connecting = connection_df.loc[column_a, column_b]
        return is_ab_connecting  # type: ignore

    @staticmethod
    def _convert_xxxxx_to_index_pairs(xxxxx: str) -> List[List[int]]:
        return [
            [
                int(xxxxx[i]),
                int(xxxxx[i + 1]),
            ]
            for i in range(len(xxxxx) - 1)
        ]

    def _check_xxxxx_is_connecting(self, xxxxx: str, columns: List[str]) -> bool:
        index_pairs = self._convert_xxxxx_to_index_pairs(xxxxx=xxxxx)

        is_xxxxx_connecting = True
        for index_pair in index_pairs:
            is_ab_connecting = self._check_ab_is_connecting(index_pair=index_pair, columns=columns, connection_df=self._connection_df)
            is_xxxxx_connecting = is_xxxxx_connecting and is_ab_connecting
            if not is_xxxxx_connecting:
                break
        return is_xxxxx_connecting

    def _check_xxxxxs_is_connecting(self, columns: List[str]) -> bool:
        xxxxxs = self._generate_xxxxxs(n_dim=self._n_dim)
        for xxxxx in xxxxxs:
            is_xxxxx_connecting = self._check_xxxxx_is_connecting(xxxxx=xxxxx, columns=columns)
            if is_xxxxx_connecting:
                return True
        return False

    def apply(self):
        self._disconnection_infos.sort(key=lambda disconnection_info: disconnection_info.p_value, reverse=True)
        for disconnection_info in self._disconnection_infos:
            columns = [disconnection_info.column1, disconnection_info.column2, *disconnection_info.condition_columns]
            if not self._check_xxxxxs_is_connecting(columns=columns):
                continue

            print(disconnection_info)
            self._connection_df.loc[disconnection_info.column1, disconnection_info.column2] = False
