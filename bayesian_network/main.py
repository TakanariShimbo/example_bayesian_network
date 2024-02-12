from typing import List

import pandas as pd
import numpy as np

from .connect import ConnectChecker
from .collector import DisconnectInfoCollector
from .applyer import DisconnectApplyer
from .closeness import ClosenessAnalyzer


class BayesianNetwork:
    def __init__(self, bin_df: pd.DataFrame, n_dim_total: int = 2):
        self._n_dim_total = n_dim_total
        self._df_columns = bin_df.columns.to_numpy()
        self._bin_df = bin_df
        self._connect_dfs: List[pd.DataFrame] = []
        self._labels: List[str] = []

        connect_init_df = self._get_init_connect_df(df_columns=self._df_columns)
        self._connect_dfs.append(connect_init_df)
        self._labels.append("Init")

    @staticmethod
    def _get_init_connect_df(df_columns: np.ndarray):
        connect_init_df = pd.DataFrame(data=False, index=df_columns, columns=df_columns, dtype=bool)

        for i, col1 in enumerate(df_columns[:-1]):
            for j in range(i + 1, len(df_columns)):
                col2 = df_columns[j]
                connect_init_df.loc[col1, col2] = True

        return connect_init_df

    @staticmethod
    def _run_step(n_dim: int, connect_checker: ConnectChecker, connect_df: pd.DataFrame):
        print(f"---------- COLECT ----------")
        collector = DisconnectInfoCollector(n_dim=n_dim, connect_df=connect_df, connect_checker=connect_checker)
        collector.run()
        print()

        print(f"---------- APPLY ----------")
        new_connect_df = connect_df.copy()
        applyer = DisconnectApplyer(n_dim=n_dim, connect_df=new_connect_df, disconnect_infos=collector._disconnect_infos)
        applyer.run()
        print()

        return new_connect_df

    def run(self, p_threshold: float = 0.05):
        connect_checker = ConnectChecker(bin_df=self._bin_df, p_threshold=p_threshold)

        for n_dim in range(self._n_dim_total + 1):
            print(f"==================== DIM{n_dim} ====================")
            new_connect_df = self._run_step(n_dim=n_dim, connect_checker=connect_checker, connect_df=self._connect_dfs[-1])
            self._connect_dfs.append(new_connect_df)
            self._labels.append(f"Level{n_dim}")

        connect_df_dict = {}
        for label, connect_df in zip(self._labels, self._connect_dfs):
            connect_df_dict[label] = connect_df

        return connect_df_dict

    def analyze(self, target_col: str):
        closeness_dfs = []
        for connect_df in self._connect_dfs:
            analyzer = ClosenessAnalyzer(connect_df=connect_df)
            closeness_df = analyzer.analyze(target_col=target_col)
            closeness_dfs.append( closeness_df )

        closeness_df_dict = {}
        for label, closeness_df in zip(self._labels, closeness_dfs):
            closeness_df_dict[label] = closeness_df

        return closeness_df_dict
