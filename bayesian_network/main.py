from typing import List

import pandas as pd
import numpy as np
from pgmpy.estimators import ConstraintBasedEstimator

from .connect import ConnectChecker
from .collector import DisconnectInfoCollector
from .applyer import DisconnectApplyer
from .viz import viz_network


class BayesianNetwork:
    def __init__(self, bin_df: pd.DataFrame, n_dim_total: int = 2) -> None:
        self._n_dim_total = n_dim_total
        self._df_columns = bin_df.columns.to_numpy()
        self._estimator = ConstraintBasedEstimator(data=bin_df)
        self._connect_dfs: List[pd.DataFrame] = []

        connect_init_df = self._get_init_connect_df(df_columns=self._df_columns)
        self._connect_dfs.append(connect_init_df)

    @staticmethod
    def _get_init_connect_df(df_columns: np.ndarray):
        connect_init_df = pd.DataFrame(data=False, index=df_columns, columns=df_columns, dtype=bool)

        for i, col1 in enumerate(df_columns[:-1]):
            for j in range(i + 1, len(df_columns)):
                col2 = df_columns[j]
                connect_init_df.loc[col1, col2] = True

        return connect_init_df

    @staticmethod
    def _run_step(n_dim: int, estimator: ConstraintBasedEstimator, connect_df: pd.DataFrame, p_threshold: float = 0.05):
        print(f"==================== DIM{n_dim} ====================")
        connect_checker = ConnectChecker(estimator=estimator, p_threshold=p_threshold)
        print()
        
        print(f"-------------------- COLECT --------------------")
        collector = DisconnectInfoCollector(n_dim=n_dim, connect_df=connect_df, connect_checker=connect_checker)
        collector.run()
        print()
        
        print(f"-------------------- APPLY --------------------")
        new_connect_df = connect_df.copy()
        applyer = DisconnectApplyer(n_dim=n_dim, connect_df=new_connect_df, disconnect_infos=collector._disconnect_infos)
        applyer.run()
        print()
        print()

        return new_connect_df

    def run(self):
        for n_dim in range(self._n_dim_total+1):
            new_connect_df = self._run_step(n_dim=n_dim, estimator=self._estimator, connect_df=self._connect_dfs[-1], p_threshold = 0.05)
            self._connect_dfs.append(new_connect_df)

    def viz(self):
        labels = ["Init"]
        for i in range(self._n_dim_total+1):
            labels.append(f"Level{i}")

        for label, connect_df in zip(labels, self._connect_dfs):
            viz_network(connect_df, f"Network {label}")