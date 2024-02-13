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

        column_names = bin_df.columns.to_list()
        init_connection_df = self._get_init_connection_df(column_names=column_names)
        self._connection_dfs.append(init_connection_df)
        self._labels.append("Init")

    @property
    def connection_df_dict(self):
        connection_df_dict_ = {}
        for label, connection_df in zip(self._labels, self._connection_dfs):
            connection_df_dict_[label] = connection_df
        return connection_df_dict_

    @staticmethod
    def _get_init_connection_df(column_names: List[str]):
        init_connection_df = pd.DataFrame(data=False, index=column_names, columns=column_names, dtype=bool)

        for i, column1 in enumerate(column_names[:-1]):
            for j in range(i + 1, len(column_names)):
                column2 = column_names[j]
                init_connection_df.loc[column1, column2] = True

        return init_connection_df

    @staticmethod
    def _analyze_connection_step(n_dim: int, connection_checker: ConnectionChecker, connection_df: pd.DataFrame):
        print(f"----------------------------------------------------")
        print(f"             Collect DisconnectionInfos             ")
        print(f"----------------------------------------------------")
        disconnection_infos_collector = DisconnectionInfosCollector(n_dim=n_dim, connection_df=connection_df, connection_checker=connection_checker)
        disconnection_infos_collector.collect()

        print(f"----------------------------------------------------")
        print(f"              Apply DisconnectionInfos              ")
        print(f"----------------------------------------------------")
        new_connect_df = connection_df.copy()
        disconnection_infos_applyer = DisconnectionInfosApplyer(n_dim=n_dim, connection_df=new_connect_df, disconnection_infos=disconnection_infos_collector._disconnection_infos)
        disconnection_infos_applyer.apply()

        return new_connect_df

    def analyze_connection(self, p_threshold: float = 0.05):
        connection_checker = ConnectionChecker(bin_df=self._bin_df, p_threshold=p_threshold)

        for n_dim in range(self._n_dim_total + 1):
            print(f"====================================================")
            print(f"                     DIM{n_dim}                     ")
            print(f"====================================================")
            new_connection_df = self._analyze_connection_step(n_dim=n_dim, connection_checker=connection_checker, connection_df=self._connection_dfs[-1])
            self._connection_dfs.append(new_connection_df)
            self._labels.append(f"Level{n_dim}")
            print()

        return self.connection_df_dict

    def analyze_closeness(self, target_col: str):
        closeness_dfs = []
        for connection_df in self._connection_dfs:
            analyzer = ClosenessAnalyzer(connection_df=connection_df)
            closeness_df = analyzer.analyze(target_column=target_col)
            closeness_dfs.append( closeness_df )

        closeness_df_dict = {}
        for label, closeness_df in zip(self._labels, closeness_dfs):
            closeness_df_dict[label] = closeness_df

        return closeness_df_dict
