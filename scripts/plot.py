import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json
import ast
from pathlib import Path

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # MacOS
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")
sns.set_palette("husl")

# 读取CSV文件
df = pd.read_csv('performance_metrics.csv')

# 将case_name简化，只保留mesh类型（fine, medium, coarse等）
df['mesh_type'] = df['case_name'].str.extract(r'Template_?(\w+)?')[0].fillna('base')

# 将final_residuals从字符串转换为字典
df['final_residuals'] = df['final_residuals'].apply(ast.literal_eval)
df['p_residual'] = df['final_residuals'].apply(lambda x: x.get('p', 0))

# 创建一个图形，包含多个子图
fig = plt.figure(figsize=(20, 12))

# 1. 计算时间分布图
plt.subplot(2, 2, 1)
time_data = df[['mesh_type', 'gmsh_to_foam_time', 'decompose_par_time', 'solver_time']]
time_data_melted = pd.melt(time_data, id_vars=['mesh_type'], 
                          var_name='操作类型', value_name='耗时(秒)')
sns.barplot(data=time_data_melted, x='mesh_type', y='耗时(秒)', hue='操作类型')
plt.title('不同网格类型的计算时间分布')
plt.xticks(rotation=45)

# 2. 总计算时间对比
plt.subplot(2, 2, 2)
sns.barplot(data=df, x='mesh_type', y='total_time')
plt.title('不同网格类型的总计算时间对比')
plt.ylabel('总时间(秒)')
plt.xticks(rotation=45)

# 3. 内存使用对比
plt.subplot(2, 2, 3)
sns.barplot(data=df, x='mesh_type', y='peak_memory_usage')
plt.title('不同网格类型的内存使用峰值')
plt.ylabel('内存使用(MB)')
plt.xticks(rotation=45)

# 4. Courant数和压力残差的关系
plt.subplot(2, 2, 4)
scatter = plt.scatter(df['max_courant_number'], df['p_residual'], 
                     c=df.index, cmap='viridis', s=100)
plt.colorbar(scatter, label='网格类型索引')
plt.title('Courant数与压力残差的关系')
plt.xlabel('最大Courant数')
plt.ylabel('压力残差')

# 调整布局
plt.tight_layout()

# 保存图片
plt.savefig('performance_analysis.png', dpi=300, bbox_inches='tight')

# 创建详细的性能指标表格可视化
plt.figure(figsize=(12, 6))
performance_metrics = pd.DataFrame({
    '网格类型': df['mesh_type'],
    '总计算时间(s)': df['total_time'].round(2),
    '最大Courant数': df['max_courant_number'].round(3),
    '压力残差': df['p_residual'].round(6),
    '内存使用(MB)': df['peak_memory_usage'].round(2)
})

# 创建表格可视化
sns.heatmap(performance_metrics.set_index('网格类型').T, 
            annot=True, fmt='.3g', cmap='YlOrRd', cbar=False)
plt.title('性能指标详细对比')
plt.tight_layout()
plt.savefig('performance_metrics_table.png', dpi=300, bbox_inches='tight')

# 输出一些统计信息
print("\n性能分析统计：")
print("-" * 50)
print(f"总计算时间最短的网格：{df.loc[df['total_time'].idxmin(), 'mesh_type']}")
print(f"内存使用最少的网格：{df.loc[df['peak_memory_usage'].idxmin(), 'mesh_type']}")
print(f"压力残差最小的网格：{df.loc[df['p_residual'].idxmin(), 'mesh_type']}")
print(f"平均计算时间：{df['total_time'].mean():.2f}秒")
