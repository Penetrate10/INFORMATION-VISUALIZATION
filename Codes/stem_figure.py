import pandas as pd
import matplotlib.pyplot as plt

# 读取数据，仅选取需要的列
mbti_df = pd.read_csv('mbti_labels.csv', usecols=['id', 'mbti_personality'])
users_df = pd.read_csv('user_info.csv', usecols=['id', 'followers_count', 'friends_count', 'favourites_count'])

# 合并数据集
merged_df = pd.merge(mbti_df, users_df, on='id')

# 计算每个MBTI类型的平均followers_count、friends_count、favourites_count
grouped_df = merged_df.groupby('mbti_personality').mean()

# 绘制stem图
plt.figure(figsize=(10, 8))

# 为每个平均值绘制茎叶
plt.stem(grouped_df.index, grouped_df['favourites_count'], linefmt='r-', markerfmt='r^', basefmt=' ', label='Average Favourites Count')
plt.stem(grouped_df.index, grouped_df['followers_count'], linefmt='b-', markerfmt='bo', basefmt=' ', label='Average Followers Count')
plt.stem(grouped_df.index, grouped_df['friends_count'], linefmt='g-', markerfmt='gs', basefmt=' ', label='Average Friends Count')

# 添加图例
plt.legend()

# 添加标题和轴标签
plt.title('Average Social Media Metrics by MBTI Type')
plt.xlabel('MBTI Type')
plt.ylabel('Average Count')

# 调整x轴标签的角度
plt.xticks(rotation=45)

# 显示图表
plt.show()
