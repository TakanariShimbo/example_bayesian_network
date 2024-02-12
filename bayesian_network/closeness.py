import pandas as pd


class ClosenessAnalyzer:
    def __init__(self, connect_df: pd.DataFrame) -> None:
        self._connect_df = connect_df
        df_columns = connect_df.columns.to_numpy()
        self._closeness_df = pd.DataFrame(data=0, index=df_columns, columns=df_columns, dtype=int)
    
    def _search_next_cols(self, current_cols, checked_cols, n):
        next_cols = []
        for col in current_cols:
            connect_series_i = self._connect_df.loc[:, col]
            closeness_series_i = self._closeness_df.loc[:, col]
            next_cols_i = connect_series_i[connect_series_i].index.to_list()
            closeness_series_i[(connect_series_i) & (closeness_series_i == 0)] = n
            
            connect_series_j = self._connect_df.loc[col, :]
            closeness_series_j = self._closeness_df.loc[col, :]
            next_cols_j = connect_series_j[connect_series_j].index.to_list()
            closeness_series_j[(connect_series_j) & (closeness_series_j == 0)] = n
            
            next_cols = [*next_cols, *next_cols_i, *next_cols_j]
        
        next_cols = list(set(next_cols) - set(checked_cols))
        checked_cols = [*checked_cols, *next_cols]
        return next_cols, checked_cols
    
    def analyze(self, target_col: str):
        next_cols = [target_col]
        checked_cols = [target_col]

        count = 1
        while len(next_cols) != 0:
            next_cols, checked_cols = self._search_next_cols(current_cols=next_cols, checked_cols=checked_cols, n=count)
            count += 1

        return self._closeness_df