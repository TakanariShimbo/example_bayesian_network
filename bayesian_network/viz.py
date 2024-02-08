import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx


def viz_network(connect_df: pd.DataFrame, title):
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
    nx.draw_networkx(G, pos, with_labels=True, arrows=False, node_size=3000, alpha=0.4, font_weight="bold")
    plt.title(title)
    plt.axis('off')