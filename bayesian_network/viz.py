import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def viz_connection(connection_df: pd.DataFrame, title: str):
    df_columns = connection_df.columns.to_list()
    
    connection_pairs = []
    for i, column1 in enumerate(df_columns[:-2]):
        for j in range(i + 1, len(df_columns)):
            column2 = df_columns[j]
            if connection_df.loc[column1, column2]:
                connection_pairs.append((column1, column2))

    G = nx.DiGraph()
    G.add_nodes_from(df_columns)
    G.add_edges_from(connection_pairs)

    pos = nx.circular_layout(G)

    plt.figure(figsize=(10, 7))
    nx.draw_networkx_nodes(G, pos, node_size=3000, alpha=0.6)
    nx.draw_networkx_labels(G, pos, font_weight="bold")
    nx.draw_networkx_edges(G, pos, arrows=False)
    plt.title(title)
    plt.axis('off')


def viz_closeness(closeness_df: pd.DataFrame, title: str):
    df_columns = closeness_df.columns.to_list()
    
    connection_pairs = []
    closenesses = []
    for i, column1 in enumerate(df_columns[:-2]):
        for j in range(i + 1, len(df_columns)):
            column2 = df_columns[j]
            if closeness_df.loc[column1, column2] > 0:
                connection_pairs.append((column1, column2))
                closenesses.append(closeness_df.loc[column1, column2])

    G = nx.DiGraph()
    G.add_nodes_from(df_columns)
    G.add_edges_from(connection_pairs)

    pos = nx.circular_layout(G)

    plt.figure(figsize=(10, 7))
    closenesses = np.array(closenesses, dtype=float)
    edge_colors = plt.cm.summer(closenesses/closenesses.max())
    nx.draw_networkx_nodes(G, pos, node_size=3000, alpha=0.6)
    nx.draw_networkx_labels(G, pos, font_weight="bold")
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, arrows=False)
    plt.title(title)
    plt.axis('off')