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
            digits_str = f"0{''.join(map(str, digits))}1"
            result.append(digits_str)
        return result

    @staticmethod
    def _check_xxxxx_connect(xxxxx: str, cols: List[str], connect_df: pd.DataFrame) -> bool:
        idx_pairs = [
            [
                int(xxxxx[i]),
                int(xxxxx[i + 1]),
            ]
            for i in range(len(xxxxx) - 1)
        ]

        is_connect = True
        for idx_pair in idx_pairs:
            idx_pair.sort()
            idx1, idx2 = idx_pair
            is_connect_: bool = connect_df.loc[cols[idx1], cols[idx2]]
            is_connect = is_connect and is_connect_
            if not is_connect:
                break
        return is_connect

    def _check_xxxxxs_connect(self, cols: List[str]) -> bool:
        xxxxxs = self._generate_xxxxxs(n_dim=self._n_dim)
        for xxxxx in xxxxxs:
            is_connect = self._check_xxxxx_connect(xxxxx=xxxxx, cols=cols, connect_df=self._connect_df)
            if is_connect:
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
