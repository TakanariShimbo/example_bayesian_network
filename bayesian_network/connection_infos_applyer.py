import itertools
from typing import List

import numpy as np
import pandas as pd

from .connection import ConnectionInfo


class ConnectionInfosApplyer:
    def __init__(self, n_dim: int, connection_df: pd.DataFrame, p_value_df: pd.DataFrame, connection_infos: List[ConnectionInfo]):
        self._n_dim = n_dim
        self._connection_df = connection_df
        self._p_value_df = p_value_df
        self._connection_infos = connection_infos

    @staticmethod
    def _generate_xxxxxs_list(n_dim: int) -> List[List[str]]:
        base_xxx_list = np.arange(n_dim) + 2
        permutations_xxx_list = list(itertools.permutations(base_xxx_list))
        xxxxxs_list = []
        for xxx_list in permutations_xxx_list:
            xxx = ''.join(map(str, xxx_list))
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
    def _convert_xxxxx_to_list(xxxxx: str) -> List[int]:
        return [int(xxxxx[i]) for i in range(len(xxxxx) - 1)]

    def _check_xxxxxs_is_connecting(self, xxxxxs: List[str], columns: List[str]) -> bool:
        is_xxxxxs_connecting = True
        for xxxxx in xxxxxs:
            xxxxx_list = self._convert_xxxxx_to_list(xxxxx=xxxxx)
            for i in range(len(xxxxx_list)-1):
                index_pair = [xxxxx_list[i], xxxxx_list[i+1]]
                is_ab_connecting = self._check_ab_is_connecting(index_pair=index_pair, columns=columns, connection_df=self._connection_df)
                is_xxxxxs_connecting = is_xxxxxs_connecting and is_ab_connecting
                if not is_xxxxxs_connecting:
                    break
        return is_xxxxxs_connecting

    def _check_xxxxxs_list_is_connecting(self, columns: List[str]) -> bool:
        xxxxxs_list = self._generate_xxxxxs_list(n_dim=self._n_dim)
        for xxxxxs in xxxxxs_list:
            is_xxxxxs_connecting = self._check_xxxxxs_is_connecting(xxxxxs=xxxxxs, columns=columns)
            if is_xxxxxs_connecting:
                return True
        return False

    def init_p_value_df(self):
        for connection_info in self._connection_infos:
            self._p_value_df.loc[connection_info.column1, connection_info.column2] = connection_info.p_value

    def filter(self):
        disconnection_infos = [info for info in self._connection_infos if not info.is_connecting]
        disconnection_infos.sort(key=lambda disconnection_info: disconnection_info.p_value, reverse=True)

        applicable_disconnection_info = []
        for disconnection_info in disconnection_infos:
            columns = [disconnection_info.column1, disconnection_info.column2, *disconnection_info.condition_columns]
            if not self._check_xxxxxs_list_is_connecting(columns=columns):
                continue

            print(disconnection_info)
            applicable_disconnection_info.append(disconnection_info)

        self._connection_infos = applicable_disconnection_info

    def apply(self):
        for disconnection_info in self._connection_infos:
            columns = [disconnection_info.column1, disconnection_info.column2, *disconnection_info.condition_columns]
            if not self._check_xxxxxs_list_is_connecting(columns=columns):
                continue

            print(disconnection_info)
            self._connection_df.loc[disconnection_info.column1, disconnection_info.column2] = False
            self._p_value_df.loc[disconnection_info.column1, disconnection_info.column2] = disconnection_info.p_value
