from typing import List, Dict

import pandas as pd

from .connection import ConnectionChecker
from .connection_infos_collector import ConnectionInfosCollector
from .connection_infos_applyer import ConnectionInfosApplyer
from .closeness_analyzer import ClosenessAnalyzer
from .network_visualizer import NetworkVisualizer


class BayesianNetwork:
    @staticmethod
    def _get_init_connection_df(column_names: List[str]) -> pd.DataFrame:
        init_connection_df = pd.DataFrame(data=False, index=column_names, columns=column_names, dtype=bool)

        for i, column1 in enumerate(column_names[:-1]):
            for j in range(i + 1, len(column_names)):
                column2 = column_names[j]
                init_connection_df.loc[column1, column2] = True

        return init_connection_df

    @staticmethod
    def _analyze_connection_step(n_dim: int, connection_checker: ConnectionChecker, connection_df: pd.DataFrame) -> pd.DataFrame:
        connection_infos_collector = ConnectionInfosCollector(n_dim=n_dim, connection_df=connection_df, connection_checker=connection_checker)
        print(f"----------------------------------------------------")
        print(f"              Collect ConnectionInfos               ")
        print(f"----------------------------------------------------")
        connection_infos = connection_infos_collector.collect()

        new_connect_df = connection_df.copy()
        connection_infos_applyer = ConnectionInfosApplyer(n_dim=n_dim, connection_df=new_connect_df, connection_infos=connection_infos)
        print(f"----------------------------------------------------")
        print(f"              Filter DisconnectionInfos             ")
        print(f"----------------------------------------------------")
        connection_infos_applyer.filter()

        print(f"----------------------------------------------------")
        print(f"              Apply DisconnectionInfos              ")
        print(f"----------------------------------------------------")
        connection_infos_applyer.apply()

        return new_connect_df

    @classmethod
    def analyze_connection(cls, bin_df: pd.DataFrame, n_dim_total: int = 2, p_threshold: float = 0.05) -> Dict[str, pd.DataFrame]:
        connection_checker = ConnectionChecker(bin_df=bin_df, p_threshold=p_threshold)

        connection_dfs: List[pd.DataFrame] = []
        labels: List[str] = []

        column_names = bin_df.columns.to_list()
        init_connection_df = cls._get_init_connection_df(column_names=column_names)
        connection_dfs.append(init_connection_df)
        labels.append("Init")

        for n_dim in range(n_dim_total+1):
            print(f"====================================================")
            print(f"                     DIM{n_dim}                     ")
            print(f"====================================================")
            new_connection_df = cls._analyze_connection_step(n_dim=n_dim, connection_checker=connection_checker, connection_df=connection_dfs[-1])
            connection_dfs.append(new_connection_df)
            labels.append(f"Level{n_dim}")
            print()

        connection_df_dict = {}
        for label, connection_df in zip(labels, connection_dfs):
            connection_df_dict[label] = connection_df
        return connection_df_dict

    @staticmethod
    def analyze_closeness(target_col: str, connection_df_dict: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        closeness_df_dict = {}
        for label, connection_df in connection_df_dict.items():
            analyzer = ClosenessAnalyzer(connection_df=connection_df)
            closeness_df = analyzer.analyze(target_column=target_col)
            closeness_df_dict[label] = closeness_df
        return closeness_df_dict

    @staticmethod
    def visualize_connection(connection_df: pd.DataFrame, title: str):
        NetworkVisualizer.visualize_connection(connection_df=connection_df, title=title)

    @staticmethod
    def visualize_closeness(closeness_df: pd.DataFrame, title: str):
        NetworkVisualizer.visualize_closeness(closeness_df=closeness_df, title=title)