import itertools
from typing import List

import numpy as np
import pandas as pd

from .connection import ConnectionInfo


class DisconnectionInfosApplyer:
    def __init__(self, n_dim: int, connection_df: pd.DataFrame, disconnection_infos: List[ConnectionInfo]):
        self._n_dim = n_dim
        self._connection_df = connection_df
        self._df_columns = connection_df.columns.to_numpy()
        self._disconnection_infos = disconnection_infos

    """
    TODO
    """
    @staticmethod
    def _generate_xxxxxs_list(n_dim: int) -> List[List[str]]:
        permutations = list(itertools.permutations(np.arange(n_dim) + 2))
        xxxxxs_list = []
        for xxxxx_list in permutations:
            xxx = ''.join(map(str, xxxxx_list))
            xxxxx = f"0{xxx}1"
            xxxxxs_list.append([xxxxx])
        return xxxxxs_list

    @staticmethod
    def _check_ab_is_connecting(index_pair: List[int], columns: List[str], connection_df: pd.DataFrame) -> bool:
        index_pair.sort()
        index_a, index_b = index_pair
        column_a = columns[index_a]
        column_b = columns[index_b]
        is_ab_connecting = connection_df.loc[column_a, column_b]
        return is_ab_connecting  # type: ignore

    @staticmethod
    def _convert_xxxxx_from_str_to_list(xxxxx: str) -> List[int]:
        return [int(xxxxx[i]) for i in range(len(xxxxx))]

    def _check_xxxxxs_is_connecting(self, xxxxxs: List[str], columns: List[str]) -> bool:
        is_xxxxx_connecting = True
        for xxxxx in xxxxxs:
            xxxxx_list = self._convert_xxxxx_from_str_to_list(xxxxx=xxxxx)
            for i in range(len(xxxxx_list)-1):
                index_pair = [index_pair[i], index_pair[i+1]]
                is_ab_connecting = self._check_ab_is_connecting(index_pair=index_pair, columns=columns, connection_df=self._connection_df)
                is_xxxxx_connecting = is_xxxxx_connecting and is_ab_connecting
                if not is_xxxxx_connecting:
                    break
        return is_xxxxx_connecting

    def _check_xxxxxs_list_is_connecting(self, columns: List[str]) -> bool:
        xxxxxs_list = self._generate_xxxxxs_list(n_dim=self._n_dim)
        for xxxxxs in xxxxxs_list:
            is_xxxxx_connecting = self._check_xxxxxs_is_connecting(xxxxxs=xxxxxs, columns=columns)
            if is_xxxxx_connecting:
                return True
        return False

    def apply(self):
        self._disconnection_infos.sort(key=lambda disconnection_info: disconnection_info.p_value, reverse=True)
        for disconnection_info in self._disconnection_infos:
            columns = [disconnection_info.column1, disconnection_info.column2, *disconnection_info.condition_columns]
            if not self._check_xxxxxs_list_is_connecting(columns=columns):
                continue

            print(disconnection_info)
            self._connection_df.loc[disconnection_info.column1, disconnection_info.column2] = False
