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
                          var_name='Operation Type', value_name='Time (s)')
sns.barplot(data=time_data_melted, x='mesh_type', y='Time (s)', hue='Operation Type')
plt.title('Computation Time Distribution for Different Mesh Types')
plt.xticks(rotation=45)

# 2. 总计算时间对比
plt.subplot(2, 2, 2)
sns.barplot(data=df, x='mesh_type', y='total_time')
plt.title('Total Computation Time Comparison')
plt.ylabel('Total Time (s)')
plt.xticks(rotation=45)

# 3. 内存使用对比
plt.subplot(2, 2, 3)
sns.barplot(data=df, x='mesh_type', y='peak_memory_usage')
plt.title('Peak Memory Usage by Mesh Type')
plt.ylabel('Memory Usage (MB)')
plt.xticks(rotation=45)

# 4. Courant数和压力残差的关系
plt.subplot(2, 2, 4)
scatter = plt.scatter(df['max_courant_number'], df['p_residual'], 
                     c=df.index, cmap='viridis', s=100)
plt.colorbar(scatter, label='Mesh Type Index')
plt.title('Relationship between Courant Number and Pressure Residual')
plt.xlabel('Maximum Courant Number')
plt.ylabel('Pressure Residual')

# 调整布局
plt.tight_layout()

# 保存图片
plt.savefig('performance_analysis.png', dpi=300, bbox_inches='tight')

# 创建详细的性能指标表格可视化
plt.figure(figsize=(12, 6))
performance_metrics = pd.DataFrame({
    'Mesh Type': df['mesh_type'],
    'Total Time (s)': df['total_time'].round(2),
    'Max Courant Number': df['max_courant_number'].round(3),
    'Pressure Residual': df['p_residual'].round(6),
    'Memory Usage (MB)': df['peak_memory_usage'].round(2)
})

# 创建表格可视化
sns.heatmap(performance_metrics.set_index('Mesh Type').T, 
            annot=True, fmt='.3g', cmap='YlOrRd', cbar=False)
plt.title('Detailed Performance Metrics Comparison')
plt.tight_layout()
plt.savefig('performance_metrics_table.png', dpi=300, bbox_inches='tight')

# 输出一些统计信息
print("\nPerformance Analysis Statistics:")
print("-" * 50)
print(f"Mesh with shortest computation time: {df.loc[df['total_time'].idxmin(), 'mesh_type']}")
print(f"Mesh with lowest memory usage: {df.loc[df['peak_memory_usage'].idxmin(), 'mesh_type']}")
print(f"Mesh with smallest pressure residual: {df.loc[df['p_residual'].idxmin(), 'mesh_type']}")
print(f"Average computation time: {df['total_time'].mean():.2f} seconds")
