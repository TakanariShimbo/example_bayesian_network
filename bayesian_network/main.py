from typing import List

import pandas as pd

from .connection import ConnectionChecker
from .disconnection_infos_collector import DisconnectionInfosCollector
from .disconnection_infos_applyer import DisconnectionInfosApplyer
from .closeness_analyzer import ClosenessAnalyzer


class BayesianNetwork:
    def __init__(self, bin_df: pd.DataFrame, n_dim_total: int = 2):
        self._n_dim_total = n_dim_total
        self._bin_df = bin_df
        self._connection_dfs: List[pd.DataFrame] = []
        self._labels: List[str] = []

        df_columns = bin_df.columns.to_list()
        init_connection_df = self._get_init_connection_df(df_columns=df_columns)
        self._connection_dfs.append(init_connection_df)
        self._labels.append("Init")

    @staticmethod
    def _get_init_connection_df(df_columns: List[str]):
        init_connection_df = pd.DataFrame(data=False, index=df_columns, columns=df_columns, dtype=bool)

        for i, column1 in enumerate(df_columns[:-1]):
            for j in range(i + 1, len(df_columns)):
                column2 = df_columns[j]
                init_connection_df.loc[column1, column2] = True

        return init_connection_df

    @staticmethod
    def _run_step(n_dim: int, connection_checker: ConnectionChecker, connection_df: pd.DataFrame):
        print(f"---------- COLECT ----------")
        disconnection_infos_collector = DisconnectionInfosCollector(n_dim=n_dim, connection_df=connection_df, connection_checker=connection_checker)
        disconnection_infos_collector.collect()
        print()

        print(f"---------- APPLY ----------")
        new_connect_df = connection_df.copy()
        disconnection_infos_applyer = DisconnectionInfosApplyer(n_dim=n_dim, connection_df=new_connect_df, disconnection_infos=disconnection_infos_collector._disconnection_infos)
        disconnection_infos_applyer.apply()
        print()

        return new_connect_df

    def run(self, p_threshold: float = 0.05):
        connection_checker = ConnectionChecker(bin_df=self._bin_df, p_threshold=p_threshold)

        for n_dim in range(self._n_dim_total + 1):
            print(f"==================== DIM{n_dim} ====================")
            new_connection_df = self._run_step(n_dim=n_dim, connection_checker=connection_checker, connection_df=self._connection_dfs[-1])
            self._connection_dfs.append(new_connection_df)
            self._labels.append(f"Level{n_dim}")

        connection_df_dict = {}
        for label, connection_df in zip(self._labels, self._connection_dfs):
            connection_df_dict[label] = connection_df

        return connection_df_dict

    def analyze(self, target_col: str):
        closeness_dfs = []
        for connect_df in self._connection_dfs:
            analyzer = ClosenessAnalyzer(connection_df=connect_df)
            closeness_df = analyzer.analyze(target_column=target_col)
            closeness_dfs.append( closeness_df )

        closeness_df_dict = {}
        for label, closeness_df in zip(self._labels, closeness_dfs):
            closeness_df_dict[label] = closeness_df

        return closeness_df_dict
