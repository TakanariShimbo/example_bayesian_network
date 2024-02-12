from typing import List

import pandas as pd


class ClosenessAnalyzer:
    def __init__(self, connection_df: pd.DataFrame) -> None:
        self._connection_df = connection_df
        df_columns = connection_df.columns.to_numpy()
        self._closeness_df = pd.DataFrame(data=0, index=df_columns, columns=df_columns, dtype=int)
    
    def _search_next_columns(self, current_columns: List[str], checked_columns: List[str], closeness_value: int):
        next_columns = []
        for column in current_columns:
            connect_series_i = self._connection_df.loc[:, column]
            closeness_series_i = self._closeness_df.loc[:, column]
            next_columns_i = connect_series_i[connect_series_i].index.to_list()
            closeness_series_i[(connect_series_i) & (closeness_series_i == 0)] = closeness_value
            
            connect_series_j = self._connection_df.loc[column, :]
            closeness_series_j = self._closeness_df.loc[column, :]
            next_columns_j = connect_series_j[connect_series_j].index.to_list()
            closeness_series_j[(connect_series_j) & (closeness_series_j == 0)] = closeness_value
            
            next_columns = [*next_columns, *next_columns_i, *next_columns_j]
        
        next_columns = list(set(next_columns) - set(checked_columns))
        checked_columns = [*checked_columns, *next_columns]
        return next_columns, checked_columns
    
    def analyze(self, target_column: str):
        next_columns = [target_column]
        checked_columns = [target_column]

        closeness_value = 1
        while len(next_columns) != 0:
            next_columns, checked_columns = self._search_next_columns(current_columns=next_columns, checked_columns=checked_columns, closeness_value=closeness_value)
            closeness_value += 1

        return self._closeness_df