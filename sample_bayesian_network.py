# %%
import warnings
warnings.simplefilter('ignore')


# %%
import numpy as np
import pandas as pd

from bayesian_network import BayesianNetwork


# %%
df_original = pd.read_csv("./data/taitanic.csv")
df_original


# %%
categorical_columns = ["Survived", "Pclass", "SibSp", "Parch", "Sex", "Embarked"]
categorical_df = df_original.loc[:, [*categorical_columns]]
categorical_df.head()


# %%
numerical_columns = ["Age", "Fare"]
numerical_df = df_original.loc[:, [*numerical_columns]]
numerical_df.head()

# %%
numerical_df['Age'] = numerical_df['Age'].fillna(numerical_df['Age'].mean())
numerical_df['Fare'] = numerical_df['Fare'].fillna(numerical_df['Fare'].mean())
numerical_df.isna().sum()


# %%
bin_df = pd.DataFrame([])
n_bin = 3
for name in numerical_df.columns:
    bin_df[name], _ = pd.cut(numerical_df[name], n_bin, labels=list(np.arange(n_bin)+1), retbins=True)
bin_df.head()


# %%
bin_df = pd.concat([categorical_df, bin_df], axis=1)
bin_df.head()


# %%
bin_df = bin_df.loc[:, bin_df.columns[::-1].to_list()]
bin_df = bin_df.dropna()
bin_df


# %%
bayesian_network = BayesianNetwork(bin_df=bin_df, n_dim_total=2)
bayesian_network.run()


# %%
bayesian_network.viz()


# %%
