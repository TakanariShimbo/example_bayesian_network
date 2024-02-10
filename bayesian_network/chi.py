from typing import List

import pandas as pd
from scipy import stats


def chi_square_test(col1: str, col2: str, cond_cols: List[str], bin_df: pd.DataFrame) -> float:
    # Step 1: Check if the arguments are valid and type conversions.
    if col1 in cond_cols:
        raise ValueError(
            f"The variables col1 or col2 can't be in cond_cols. Found {col1} in cond_cols."
        )
    if col2 in cond_cols:
        raise ValueError(
            f"The variables col1 or col2 can't be in cond_cols. Found {col2} in cond_cols."
        )

    # Step 2: Do contingency test.
    if len(cond_cols) == 0:
        # Do a simple contingency test if there are no conditional variables.
        chi, p_value, dof, _ = stats.chi2_contingency(
            bin_df.groupby([col1, col2]).size().unstack(col2, fill_value=0), lambda_="pearson"
        )

    else:
        # If there are conditionals variables, iterate over unique states and do the contingency test.
        chi = 0
        dof = 0
        for parsed_cond, parsed_bin_df in bin_df.groupby(cond_cols):
            try:
                chi_i, _, dof_i, _ = stats.chi2_contingency(
                    parsed_bin_df.groupby([col1, col2]).size().unstack(col2, fill_value=0), lambda_="pearson"
                )
                chi += chi_i
                dof += dof_i
            except ValueError:
                # If one of the values is 0 in the 2x2 table.
                # if isinstance(parsed_cond, str):
                #     parsed_cond_str = f"{cond_cols[0]}={parsed_cond}"
                # else:
                #     parsed_cond_str = ", ".join(
                #         [f"{var}={state}" for var, state in zip(cond_cols, parsed_cond)]
                #     )
                # print(
                #     f"Skipping the test {col1} \u27C2 {col2} | {parsed_cond_str}. Not enough samples"
                # )
                pass
        p_value = 1 - stats.chi2.cdf(chi, df=dof)

    # Step 3: Return the values
    return p_value   # type: ignore


