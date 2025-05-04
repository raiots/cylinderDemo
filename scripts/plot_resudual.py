import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from numpy.lib.stride_tricks import sliding_window_view
import os

"""
绘制残差对比图
"""

def moving_average(data, window_size):
    """计算移动平均"""
    # 确保窗口大小是整数且至少为1
    window_size = max(1, int(window_size))
    weights = np.ones(window_size) / window_size
    return np.convolve(data, weights, mode='valid')

def read_residuals(file_path):
    """读取单个文件的残差数据"""
    T = []  # 时间
    P = []  # 压力残差
    U = []  # x方向速度残差
    V = []  # y方向速度残差
    nut = []  # 湍流场残差
    
    try:
        with open(file_path, 'r') as f:
            # 首先计算每个时间步的迭代次数
            p_cnt = 0
            U_cnt = 0
            nut_cnt = 0
            
            # 读取第一个时间步来计算迭代次数
            for line in f:
                if line.startswith('Time ='):
                    while True:
                        line = next(f, None)
                        if line is None:
                            break
                        if 'Solving for p' in line:
                            p_cnt += 1
                        if 'Solving for Ux' in line:
                            U_cnt += 1
                        if 'Solving for nuTilda' in line:
                            nut_cnt += 1
                        if line.startswith('Time ='):
                            break
                    break
            
            # 回到文件开头
            f.seek(0)
            
            current_time = 0.0
            # 读取所有残差值
            for line in f:
                if line.startswith('Time ='):
                    try:
                        current_time = float(line.split('=')[1].strip())
                        T.append(current_time)
                    except:
                        pass
                elif 'Solving for p' in line:
                    residual = float(line.split(',')[1].split()[-1])
                    P.append(residual)
                elif 'Solving for Ux' in line:
                    residual = float(line.split(',')[1].split()[-1])
                    U.append(residual)
                elif 'Solving for Uy' in line:
                    residual = float(line.split(',')[1].split()[-1])
                    V.append(residual)
                elif 'Solving for nuTilda' in line:
                    residual = float(line.split(',')[1].split()[-1])
                    nut.append(residual)
        
        return {
            'T': np.array(T),
            'P': np.array(P),
            'U': np.array(U),
            'V': np.array(V),
            'nut': np.array(nut),
            'p_cnt': p_cnt,
            'U_cnt': U_cnt,
            'nut_cnt': nut_cnt
        }
    
    except FileNotFoundError:
        print(f"警告: 文件 {file_path} 未找到")
        return None

# 指定输入文件
files = [
    "data/task_2D_Cylinder_Template_fine/log.mpiexec",
    "data/task_2D_Cylinder_Template/log.mpiexec",
    "data/task_2D_Cylinder_Template_coarse/log.mpiexec"
]

# 读取所有文件的数据
all_data = []
for file_path in files:
    data = read_residuals(file_path)
    if data is not None:
        all_data.append((os.path.basename(os.path.dirname(file_path)), data))

if not all_data:
    print("没有找到有效的数据文件")
    exit(1)

# 设置绘图样式
sns.set_style("whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(20, 10))  # 2:1的宽高比

# 定义颜色方案
colors = ['k', 'r', 'b', 'g']

# 设置共同的x轴范围
x_min, x_max = 0, 5  # 0-5秒

# 首先计算所有滤波后的数据
smoothed_data = []
for case_name, data in all_data:
    # 对每个变量进行滤波
    P = data['P']
    U = data['U']
    V = data['V']
    nut = data['nut']
    
    window_size_p = int(len(P) * 0.001)
    window_size_u = int(len(U) * 0.001)
    window_size_v = int(len(V) * 0.001)
    window_size_nut = int(len(nut) * 0.001)
    
    P_smooth = moving_average(P, window_size_p)
    U_smooth = moving_average(U, window_size_u)
    V_smooth = moving_average(V, window_size_v)
    nut_smooth = moving_average(nut, window_size_nut)
    
    smoothed_data.append({
        'case_name': case_name,
        'P_smooth': P_smooth,
        'U_smooth': U_smooth,
        'V_smooth': V_smooth,
        'nut_smooth': nut_smooth
    })

# 找到滤波后数据的最大最小值
all_smoothed_residuals = []
for data in smoothed_data:
    all_smoothed_residuals.extend([
        data['P_smooth'].min(), data['P_smooth'].max(),
        data['U_smooth'].min(), data['U_smooth'].max(),
        data['V_smooth'].min(), data['V_smooth'].max(),
        data['nut_smooth'].min(), data['nut_smooth'].max()
    ])
y_min, y_max = min(all_smoothed_residuals), max(all_smoothed_residuals)

# 绘制压力残差对比 (左上)
ax = axes[0, 0]
for i, smooth_data in enumerate(smoothed_data):
    case_name = smooth_data['case_name']
    P_smooth = smooth_data['P_smooth']
    x = np.linspace(0, x_max, len(P_smooth))
    ax.semilogy(x, P_smooth, color=colors[i], label=f'{case_name}', linewidth=1)
ax.set_title('Pressure Residuals', fontsize=12)
ax.set_xlabel('Time (s)', fontsize=10)
ax.set_ylabel('Residual', fontsize=10)
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.legend()
ax.grid(True)

# 绘制Ux残差对比 (右上)
ax = axes[0, 1]
for i, smooth_data in enumerate(smoothed_data):
    case_name = smooth_data['case_name']
    U_smooth = smooth_data['U_smooth']
    x = np.linspace(0, x_max, len(U_smooth))
    ax.semilogy(x, U_smooth, color=colors[i], label=f'{case_name}', linewidth=1)
ax.set_title('Velocity-x Residuals', fontsize=12)
ax.set_xlabel('Time (s)', fontsize=10)
ax.set_ylabel('Residual', fontsize=10)
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.legend()
ax.grid(True)

# 绘制Uy残差对比 (左下)
ax = axes[1, 0]
for i, smooth_data in enumerate(smoothed_data):
    case_name = smooth_data['case_name']
    V_smooth = smooth_data['V_smooth']
    x = np.linspace(0, x_max, len(V_smooth))
    ax.semilogy(x, V_smooth, color=colors[i], label=f'{case_name}', linewidth=1)
ax.set_title('Velocity-y Residuals', fontsize=12)
ax.set_xlabel('Time (s)', fontsize=10)
ax.set_ylabel('Residual', fontsize=10)
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.legend()
ax.grid(True)

# 绘制nuTilda残差对比 (右下)
ax = axes[1, 1]
for i, smooth_data in enumerate(smoothed_data):
    case_name = smooth_data['case_name']
    nut_smooth = smooth_data['nut_smooth']
    x = np.linspace(0, x_max, len(nut_smooth))
    ax.semilogy(x, nut_smooth, color=colors[i], label=f'{case_name}', linewidth=1)
ax.set_title('Turbulent Viscosity Residuals', fontsize=12)
ax.set_xlabel('Time (s)', fontsize=10)
ax.set_ylabel('Residual', fontsize=10)
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.legend()
ax.grid(True)

# 调整布局
plt.tight_layout()

# 保存图片
plt.savefig('residuals_comparison.png', dpi=300, bbox_inches='tight')