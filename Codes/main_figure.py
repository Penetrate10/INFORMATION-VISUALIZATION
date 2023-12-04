import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import scipy as sp

# 1. 读取数据
edges_df = pd.read_csv('edges.csv')
mbti_df = pd.read_csv('mbti_labels.csv')

# 2. 创建一个空的图
G = nx.Graph()

# 3. 添加互相关注的边
for _, row in edges_df.iterrows():
    if (row['follower_id'], row['followee_id']) in edges_df[['followee_id', 'follower_id']].values:
        if row['follower_id'] in mbti_df['id'].values and row['followee_id'] in mbti_df['id'].values:
            G.add_edge(row['follower_id'], row['followee_id'])

# 4. 设置边的颜色为橙色
edge_color = 'orange'

# 5. 设置所有点的颜色为蓝色，点的大小相同
node_color = 'blue'
node_size = 30

# 6. 过滤度数小于10的节点
nodes_to_remove = [node for node in G.nodes() if G.degree[node] < 10]
G.remove_nodes_from(nodes_to_remove)

# 7. 只保留最大的子图
largest_subgraph = max(nx.connected_components(G), key=len)
G_sub = G.subgraph(largest_subgraph).copy()

nodes_to_remove = [node for node in G_sub.nodes() if G_sub.degree[node] < 10]
G_sub.remove_nodes_from(nodes_to_remove)

# 8. 绘制图形
plt.figure(figsize=(10, 10))
pos = nx.spring_layout(G_sub, k=0.3)  # 调整布局以改善节点之间的间距

# 绘制边
nx.draw_networkx_edges(G_sub, pos, edge_color=edge_color, alpha=0.5)

# 绘制点
nx.draw_networkx_nodes(G_sub, pos, node_color=node_color, node_size=node_size)

# 对度数小于5的节点标注性格类型
for node in G_sub.nodes():
    if G_sub.degree(node) < 5:
        plt.annotate(mbti_df[mbti_df['id'] == node]['mbti_personality'].values[0], (pos[node][0], pos[node][1]), fontsize=10, ha='center', va='center')

# 虚拟绘制项，仅用于图例显示
plt.plot([], [], 'o', color=node_color, label='User')
plt.plot([], [], '-', color=edge_color, label='Two users follow each other.')

# 添加图例
plt.legend(loc="upper left")

# 输出节点个数
print("节点个数:", len(G_sub.nodes()))

plt.show()
