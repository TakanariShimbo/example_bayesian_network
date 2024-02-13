from typing import List, Optional

import numpy as np
import pandas as pd
from scipy import stats


def chi_square_test(column1: str, column2: str, condition_columns: List[str], bin_df: pd.DataFrame) -> Optional[float]:
    # Step 1: Check if the arguments are valid and type conversions.
    if column1 in condition_columns:
        raise ValueError(f"The variables column1 or column2 can't be in condition_columns. Found {column1} in condition_columns.")
    if column2 in condition_columns:
        raise ValueError(f"The variables column1 or column2 can't be in condition_columns. Found {column2} in condition_columns.")

    # Step 2: Do contingency test.
    if len(condition_columns) == 0:
        # Do a simple contingency test if there are no conditional variables.
        chi, p_value, dof, _ = stats.chi2_contingency(bin_df.groupby([column1, column2]).size().unstack(column2, fill_value=0), lambda_="pearson")

    else:
        # If there are conditionals variables, iterate over unique states and do the contingency test.
        chi = 0
        dof = 0
        for current_condition, parsed_bin_df in bin_df.groupby(condition_columns):
            try:
                chi_i, _, dof_i, _ = stats.chi2_contingency(parsed_bin_df.groupby([column1, column2]).size().unstack(column2, fill_value=0), lambda_="pearson")
                chi += chi_i
                dof += dof_i
            except ValueError:
                # # If one of the values is 0 in the 2x2 table.
                # if isinstance(current_condition, str):
                #     parsed_cond_str = f"{condition_columns[0]}={current_condition}"
                # else:
                #     parsed_cond_str = ", ".join(
                #         [f"{var}={state}" for var, state in zip(condition_columns, current_condition)]
                #     )
                # print(
                #     f"Skipping the test {column1} \u27C2 {column2} | {parsed_cond_str}. Not enough samples"
                # )
                pass
        p_value = 1 - stats.chi2.cdf(chi, df=dof)

    # Step 3: Return the values
    if np.isnan(p_value):
        return None

    return p_value  # type: ignore
