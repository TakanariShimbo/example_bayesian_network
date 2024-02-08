# %%
import warnings
warnings.simplefilter('ignore')


# %%
import numpy as np
import pandas as pd

from pgmpy.estimators import ConstraintBasedEstimator

from bayesian_network import ConnectChecker, DisconnectInfoCollector, DisconnectApplyer, viz_network


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
estimator = ConstraintBasedEstimator(data=bin_df)
connect_dfs = []


# %%
# Init
df_columns = bin_df.columns.to_numpy()
connect_init_df = pd.DataFrame(data=False, index=df_columns, columns=df_columns, dtype=bool)

for i, col1 in enumerate(df_columns[:-1]):
    for j in range(i + 1, len(df_columns)):
        col2 = df_columns[j]
        connect_init_df.loc[col1, col2] = True

connect_dfs.append(connect_init_df)


# %%
# loop
n_dim_total = 4
for n_dim in range(n_dim_total+1):
    
    print(f"==================== DIM{n_dim} ====================")
    connect_checker = ConnectChecker(estimator=estimator, p_threshold=0.05)
    print()
    
    print(f"-------------------- COLECT --------------------")
    collector = DisconnectInfoCollector(n_dim=n_dim, connect_df=connect_dfs[-1], connect_checker=connect_checker)
    collector.run()
    print()
    
    print(f"-------------------- APPLY --------------------")
    connect_dfs.append( connect_dfs[-1].copy() )
    applyer = DisconnectApplyer(n_dim=n_dim, connect_df=connect_dfs[-1], disconnect_infos=collector._disconnect_infos)
    applyer.run()
    print()
    print()


# %%
def highlight_true(val):
    background_color = 'green' if val == 1 else ''
    return f'background-color: {background_color}'


labels = ["init"]
for i in range(n_dim_total+1):
    labels.append(f"level{i}")


# %%
for label, connect_df in zip(labels, connect_dfs):
    viz_network(connect_df, f"Network ({label})")


# %%
