import pandas as pd
import networkx as nx
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 读取数据
edges_df = pd.read_csv('edges.csv')
mbti_df = pd.read_csv('mbti_labels.csv')

# 创建一个空的图
G = nx.Graph()

# 添加互相关注的边
for _, row in edges_df.iterrows():
    if (row['follower_id'], row['followee_id']) in edges_df[['followee_id', 'follower_id']].values:
        if row['follower_id'] in mbti_df['id'].values and row['followee_id'] in mbti_df['id'].values:
            G.add_edge(row['follower_id'], row['followee_id'])

# 初始化MBTI类型的互相关注量计数器
mbti_interactions = {mbti: 0 for mbti in mbti_df['mbti_personality'].unique()}
mbti_user_counts = {mbti: 0 for mbti in mbti_df['mbti_personality'].unique()}

# 计算互相关注量
for _, row in mbti_df.iterrows():
    user_id = row['id']
    mbti_type = row['mbti_personality']
    # 只计算该MBTI类型的用户的互相关注量
    if user_id in G.nodes:
        mutual_follows = sum(1 for neighbor in G.neighbors(user_id) if G.has_edge(neighbor, user_id))
        mbti_interactions[mbti_type] += mutual_follows
        mbti_user_counts[mbti_type] += 1

# 计算平均互相关注量
average_interactions = {mbti: (interactions / mbti_user_counts[mbti] if mbti_user_counts[mbti] else 0)
                        for mbti, interactions in mbti_interactions.items()}

# 生成词云图
wordcloud = WordCloud(width=1000, height=800, background_color='white').generate_from_frequencies(average_interactions)

# 显示词云图
plt.figure(figsize=(10, 8))
plt.imshow(wordcloud, interpolation='nearest')
plt.axis('off')
plt.show()
