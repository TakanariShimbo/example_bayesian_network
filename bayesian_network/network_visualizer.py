import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


class NetworkVisualizer:
    @staticmethod
    def visualize_connection(connection_df: pd.DataFrame, title: str):
        column_names = connection_df.columns.to_list()
        
        connection_pairs = []
        for i, column1 in enumerate(column_names[:-2]):
            for j in range(i + 1, len(column_names)):
                column2 = column_names[j]
                if connection_df.loc[column1, column2]:
                    connection_pairs.append((column1, column2))

        G = nx.DiGraph()
        G.add_nodes_from(column_names)
        G.add_edges_from(connection_pairs)
        pos = nx.circular_layout(G)

        plt.figure(figsize=(10, 7))
        nx.draw_networkx_nodes(G, pos, node_size=3000, alpha=0.6)
        nx.draw_networkx_labels(G, pos, font_weight="bold")
        nx.draw_networkx_edges(G, pos, arrows=False)
        plt.title(title)
        plt.axis('off')

    @staticmethod
    def visualize_closeness(closeness_df: pd.DataFrame, title: str):
        column_names = closeness_df.columns.to_list()
        
        connection_pairs = []
        closenesses = []
        for i, column1 in enumerate(column_names[:-2]):
            for j in range(i + 1, len(column_names)):
                column2 = column_names[j]
                if closeness_df.loc[column1, column2] > 0:
                    connection_pairs.append((column1, column2))
                    closenesses.append(closeness_df.loc[column1, column2])

        closenesses = np.array(closenesses, dtype=float)
        edge_colors = plt.colormaps["plasma"]((closenesses-1)/2)

        G = nx.DiGraph()
        G.add_nodes_from(column_names)
        G.add_edges_from(connection_pairs)
        pos = nx.circular_layout(G)

        plt.figure(figsize=(10, 7))
        nx.draw_networkx_nodes(G, pos, node_size=3000, alpha=0.6)
        nx.draw_networkx_labels(G, pos, font_weight="bold")
        nx.draw_networkx_edges(G, pos, edge_color=edge_colors, arrows=False)
        plt.title(title)
        plt.axis('off')