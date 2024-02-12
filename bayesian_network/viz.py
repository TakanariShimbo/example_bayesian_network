import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def viz_connect(connect_df: pd.DataFrame, title: str):
    df_columns = connect_df.columns.to_numpy()
    
    connect_pairs = []
    for i, col1 in enumerate(df_columns[:-2]):
        for j in range(i + 1, len(df_columns)):
            col2 = df_columns[j]
            if connect_df.loc[col1, col2]:
                connect_pairs.append((col1, col2))

    G = nx.DiGraph()
    G.add_nodes_from(df_columns)
    G.add_edges_from(connect_pairs)

    pos = nx.circular_layout(G)

    plt.figure(figsize=(10, 7))
    nx.draw_networkx_nodes(G, pos, node_size=3000, alpha=0.6)
    nx.draw_networkx_labels(G, pos, font_weight="bold")
    nx.draw_networkx_edges(G, pos, arrows=False)
    plt.title(title)
    plt.axis('off')


def viz_closeness(closeness_df: pd.DataFrame, title: str):
    df_columns = closeness_df.columns.to_numpy()
    
    connect_pairs = []
    closenesses = []
    for i, col1 in enumerate(df_columns[:-2]):
        for j in range(i + 1, len(df_columns)):
            col2 = df_columns[j]
            if closeness_df.loc[col1, col2] > 0:
                connect_pairs.append((col1, col2))
                closenesses.append(closeness_df.loc[col1, col2])
    closenesses = np.array(closenesses, dtype=float)

    G = nx.DiGraph()
    G.add_nodes_from(df_columns)
    G.add_edges_from(connect_pairs)

    pos = nx.circular_layout(G)

    plt.figure(figsize=(10, 7))
    colors = plt.cm.summer(closenesses/closenesses.max())
    nx.draw_networkx_nodes(G, pos, node_size=3000, alpha=0.6)
    nx.draw_networkx_labels(G, pos, font_weight="bold")
    nx.draw_networkx_edges(G, pos, edge_color=colors, arrows=False)
    plt.title(title)
    plt.axis('off')