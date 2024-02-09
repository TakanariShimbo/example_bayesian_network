# # 一次独立の確認
# disconnect_infos = []

# for i, col1 in enumerate(df_columns[:-2]):
#     for j in range(i + 1, len(df_columns)):
#         col2 = df_columns[j]
#         for k in range(j + 1, len(df_columns)):
#             col3 = df_columns[k]
            
#             is1to2 = connect_level0_df.loc[col1, col2]
#             is1to3 = connect_level0_df.loc[col1, col3]
#             is2to3 = connect_level0_df.loc[col2, col3]
#             if not (is1to2 and is1to3 and is2to3):
#                 print(f"{col1} {col2} {col3} skipped\n")
#                 continue
                
#             connect_info = connect_checker.check(col1, col2, [col3])
#             if not connect_info.is_connect:
#                 disconnect_infos.append(connect_info)
                
#             connect_info = connect_checker.check(col1, col3, [col2])
#             if not connect_info.is_connect:
#                 disconnect_infos.append(connect_info)
                
#             connect_info = connect_checker.check(col2, col3, [col1])
#             if not connect_info.is_connect:
#                 disconnect_infos.append(connect_info)
                
#             print(f"{col1} {col2} {col3} caluced\n")a



# # 一次独立の確認
# connect_level1_df = connect_level0_df.copy()

# for i, col1 in enumerate(df_columns[:-2]):
#     for j in range(i + 1, len(df_columns)):
#         col2 = df_columns[j]
#         for k in range(j + 1, len(df_columns)):
#             col3 = df_columns[k]
#             is1to2 = connect_level0_df.loc[col1, col2]
#             is2to3 = connect_level0_df.loc[col2, col3]
#             is3to1 = connect_level0_df.loc[col1, col3]
#             if not (is1to2 and is2to3 and is3to1):
#                 continue
                
#             print()
#             print(f"{col1} {col2} {col3}")
            
#             is_connect, independence = connect_checker.check(col1, col3, [col2])
#             if not is_connect:
#                 print(f"(1) {col1} {col3} is not connented o {col2}")
#                 connect_level1_df.loc[col1, col3] = False
#                 continue
                
#             is_connect, independence = connect_checker.check(col2, col3, [col1])
#             if not is_connect:
#                 print(f"(2) {col2} {col3} is not connented in {col1}")
#                 connect_level1_df.loc[col2, col3] = False
#                 continue
                
#             is_connect, independence = connect_checker.check(col1, col2, [col3])
#             if not is_connect:
#                 print(f"(3) {col1} {col2} is not connented in {col3}")
#                 connect_level1_df.loc[col1, col2] = False
#                 continue
            
#             print("Not Updated")

# connect_level1_df



# # 一次独立の確認
# connect_level1_df = connect_level0_df.copy()

# for i, col1 in enumerate(df_columns[:-2]):
#     for j in range(i + 1, len(df_columns)):
#         col2 = df_columns[j]
#         for k in range(j + 1, len(df_columns)):
#             col3 = df_columns[k]
#             is1to2 = connect_level0_df.loc[col1, col2]
#             is1to3 = connect_level0_df.loc[col1, col3]
#             is2to3 = connect_level0_df.loc[col2, col3]
#             if not (is1to2 and is1to3 and is2to3):
#                 continue
            
#             is1to2on3, independence_1to2on3 = connect_checker.check(col1, col2, [col3])
#             is1to3on2, independence_1to3on2 = connect_checker.check(col1, col3, [col2])
#             is2to3on1, independence_2to3on1 = connect_checker.check(col2, col3, [col1])
#             if is1to2on3 and is1to3on2 and is2to3on1:
#                 continue

#             independences = np.array([independence_1to2on3, independence_1to3on2, independence_2to3on1])
#             idx = np.argmax(independences)
#             if idx == 0:
#                 connect_level1_df.loc[col1, col2] = False
#             elif idx == 1:
#                 connect_level1_df.loc[col1, col3] = False
#             elif idx == 2:
#                 connect_level1_df.loc[col2, col3] = False

# connect_level1_df



# skel, seperating_sets = est.estimate_skeleton(significance_level=0.01)
# print("Undirected edges: ", skel.edges())

# pdag = est.skeleton_to_pdag(skel, seperating_sets)
# print("PDAG edges:", pdag.edges())

# model = est.pdag_to_dag(pdag)
# print("DAG edges:", model.edges())

# G = nx.DiGraph(pdag.edges())

# # グラフのレイアウトを計算
# pos = nx.circular_layout(G)

# # グラフを描画
# plt.figure(figsize=(10, 7))
# nx.draw_networkx(G, pos, with_labels=True, arrows=False, node_size=4000, alpha=0.4, font_weight="bold")
# plt.title("Directed Bayesian Network Visualization")
# plt.axis('off')
# plt.show()