from typing import List

from pgmpy.estimators import ConstraintBasedEstimator
from pgmpy.estimators.CITests import chi_square


class ConnectInfo:
    def __init__(self, p_val: float, col1: str, col2: str, cond_cols: List[str] = [], p_threshold: float = 0.05):
        self.is_connect = p_val < p_threshold
        self.p_val = p_val
        self.col1 = col1
        self.col2 = col2
        self.cond_cols = cond_cols
    
    def __str__(self) -> str:
        return f"{self.col1} , {self.col2} | {self.cond_cols} -> {self.is_connect} [{self.p_val:.2f}]"
    
    def __repr__(self) -> str:
        return f"{self.col1} , {self.col2} | {self.cond_cols} -> {self.is_connect} [{self.p_val:.2f}]"


class ConnectChecker:
    def __init__(self, estimator: ConstraintBasedEstimator, p_threshold: float = 0.05):
        self._estimator = estimator
        self._p_threshold = p_threshold
        
    def check(self, col1: str, col2: str, cond_cols: List[str] = []) -> ConnectInfo:
        _, p_val =  chi_square(X=col1, Y=col2, Z=cond_cols, data=self._estimator.data, state_names=self._estimator.state_names)
        connect_info = ConnectInfo(p_val, col1, col2, cond_cols=cond_cols, p_threshold=self._p_threshold)
        return connect_info