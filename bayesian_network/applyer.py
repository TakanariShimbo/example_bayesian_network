import itertools
from typing import List

import numpy as np
import pandas as pd

from .base import ConnectInfo


class DisconnectApplyer:
    def __init__(self, n_dim: int, connect_df: pd.DataFrame, disconnect_infos: List[ConnectInfo]):
        self._n_dim = n_dim
        self._connect_df = connect_df
        self._df_columns = connect_df.columns.to_numpy()
        self._disconnect_infos = disconnect_infos

    @staticmethod
    def _generate_xxxxxs(n_dim: int):
        permus = list(itertools.permutations(np.arange(n_dim) + 2))
        result = []
        for digits in permus:
            middle_digits_str = ''.join(map(str, digits))
            digits_str = f"0{middle_digits_str}1"
            result.append(digits_str)
        return result

    @staticmethod
    def _check_ab_connect(idx_pair: List[int], cols: List[str], connect_df: pd.DataFrame) -> bool:
        idx_pair.sort()
        idx_a, idx_b = idx_pair
        col_a = cols[idx_a]
        col_b = cols[idx_b]
        is_ab_connect = connect_df.loc[col_a, col_b]
        return is_ab_connect  # type: ignore

    @staticmethod
    def _convert_xxxxx_to_idx_pairs(xxxxx: str) -> List[List[int]]:
        return [
            [
                int(xxxxx[i]),
                int(xxxxx[i + 1]),
            ]
            for i in range(len(xxxxx) - 1)
        ]

    def _check_xxxxx_connect(self, xxxxx: str, cols: List[str]) -> bool:
        idx_pairs = self._convert_xxxxx_to_idx_pairs(xxxxx=xxxxx)

        is_xxxxx_connect = True
        for idx_pair in idx_pairs:
            is_ab_connect = self._check_ab_connect(idx_pair=idx_pair, cols=cols, connect_df=self._connect_df)
            is_xxxxx_connect = is_xxxxx_connect and is_ab_connect
            if not is_xxxxx_connect:
                break
        return is_xxxxx_connect

    def _check_xxxxxs_connect(self, cols: List[str]) -> bool:
        xxxxxs = self._generate_xxxxxs(n_dim=self._n_dim)
        for xxxxx in xxxxxs:
            is_xxxxx_connect = self._check_xxxxx_connect(xxxxx=xxxxx, cols=cols)
            if is_xxxxx_connect:
                return True
        return False

    def run(self):
        self._disconnect_infos.sort(key=lambda x: x.p_val, reverse=True)
        for connect_info in self._disconnect_infos:
            cols = [connect_info.col1, connect_info.col2, *connect_info.cond_cols]
            if not self._check_xxxxxs_connect(cols=cols):
                continue

            print(connect_info)
            self._connect_df.loc[connect_info.col1, connect_info.col2] = False
