import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import os
import re

def read_force_data(file_path):
    """读取力数据文件"""
    time = []
    total_force = []  # 总力
    pressure_force = []  # 压力
    viscous_force = []  # 粘性力
    
    try:
        with open(file_path, 'r') as f:
            # 跳过前4行标题
            for _ in range(4):
                next(f)
            
            # 读取数据
            for line in f:
                data = line.strip().split()
                if len(data) < 10:  # 确保行有足够的数据
                    continue
                
                # 获取时间
                time.append(float(data[0]))
                
                # 获取力数据
                total_force.append([float(data[1]), float(data[2]), float(data[3])])
                pressure_force.append([float(data[4]), float(data[5]), float(data[6])])
                viscous_force.append([float(data[7]), float(data[8]), float(data[9])])
    
    except FileNotFoundError:
        print(f"警告: 文件 {file_path} 未找到")
        return None, None, None, None
    
    return (np.array(time), 
            np.array(total_force), 
            np.array(pressure_force), 
            np.array(viscous_force))

def FFT_analysis(signal, dt):
    """进行FFT分析"""
    n = len(signal)
    yf = fft(signal)
    xf = fftfreq(n, dt)[:n//2]
    
    # 计算方差
    var = 2.0/n * np.abs(yf[0:n//2])
    
    return xf, var

def plot_forces(time, total_force, pressure_force, viscous_force, save_path=None):
    """绘制力的时间历程"""
    # 设置Seaborn样式
    sns.set_style("whitegrid")
    
    # 创建图形
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    # 绘制Fx
    ax1.plot(time, total_force[:, 0], '-r', label='Total', linewidth=1)
    ax1.plot(time, pressure_force[:, 0], '-b', label='Pressure', linewidth=1)
    ax1.plot(time, viscous_force[:, 0], '-g', label='Viscous', linewidth=1)
    ax1.axvline(x=0.1, color='black', linestyle='-', alpha=0.5)
    ax1.set_title('Force in x direction')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Force [N]')
    ax1.legend()
    
    # 绘制Fy
    ax2.plot(time, total_force[:, 1], '-r', label='Total', linewidth=1)
    ax2.plot(time, pressure_force[:, 1], '-b', label='Pressure', linewidth=1)
    ax2.plot(time, viscous_force[:, 1], '-g', label='Viscous', linewidth=1)
    ax2.axvline(x=0.1, color='black', linestyle='-', alpha=0.5)
    ax2.set_title('Force in y direction')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Force [N]')
    ax2.legend()
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图片
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig, (ax1, ax2)

def plot_fft(freq, var, save_path=None):
    """绘制FFT分析结果"""
    # 设置Seaborn样式
    sns.set_style("whitegrid")
    
    # 创建图形
    plt.figure(figsize=(10, 6))
    plt.semilogx(freq, var, color='red', alpha=0.9)
    plt.title('FFT Analysis of Forces')
    plt.ylabel('Variance [N]')
    plt.xlabel('Frequency [Hz]')
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图片
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

def calculate_statistics(F):
    """计算力的统计特性"""
    # 计算平均值和RMS
    F_avg = np.mean(F, axis=0)
    F_rms = np.sqrt(np.var(F, axis=0))
    
    # 计算系数（使用与MATLAB相同的参数）
    rho = 1.225  # 密度
    U = 5.0      # 速度
    h = 0.15     # 高度
    w = 0.075    # 宽度
    
    C_avg = F_avg / (0.5 * rho * U**2 * h * w)
    C_rms = F_rms / (0.5 * rho * U**2 * h * w)
    
    return F_avg, F_rms, C_avg, C_rms

def get_mesh_type(file_path):
    """从文件路径中提取CFL文件夹名称"""
    match = re.search(r'data/(task_cfl_\d+)', file_path)
    if match:
        return match.group(1)
    return 'default'

def main():
    # 指定输入文件
    base_path = "data/"
    mesh_types = ["task_cfl_1", "task_cfl_5", "task_cfl_20", "task_cfl_50"]  # 空字符串代表默认网格
    files = [f"{base_path}{mesh_type}/postProcessing/forces/0/force_0.dat" for mesh_type in mesh_types]
    
    # 创建图形
    fig_forces, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    fig_fft = plt.figure(figsize=(10, 6))
    ax_fft = fig_fft.add_subplot(111)
    
    # 定义不同网格类型的线型和颜色
    colors = ['k', 'r', 'b', 'g']  # 为每个CFL值定义不同的颜色
    styles = {
        'task_cfl_1': {'color': colors[0], 'linestyle': '-', 'label': 'CFL = 1'},
        'task_cfl_5': {'color': colors[1], 'linestyle': '-', 'label': 'CFL = 5'},
        'task_cfl_20': {'color': colors[2], 'linestyle': '-', 'label': 'CFL = 20'},
        'task_cfl_50': {'color': colors[3], 'linestyle': '-', 'label': 'CFL = 50'}
    }
    
    # 抽样间隔
    sample_interval = 10
    
    # 处理每个文件
    for file_path in files:
        print(file_path)
        # 使用正则表达式提取网格类型
        mesh_type = get_mesh_type(file_path)
        print(f"\n处理 {mesh_type} 网格的数据...")
        
        # 读取数据
        time, total_force, pressure_force, viscous_force = read_force_data(file_path)
        if time is None:
            continue
            
        # 数据抽样
        time = time[::sample_interval]
        total_force = total_force[::sample_interval]
        pressure_force = pressure_force[::sample_interval]
        viscous_force = viscous_force[::sample_interval]
        
        print(f"数据点数: 原始 {len(total_force) * sample_interval} -> 抽样后 {len(total_force)}")
        
        # 绘制力的时间历程
        style = styles[mesh_type]
        ax1.plot(time, total_force[:, 0], **style)
        ax2.plot(time, total_force[:, 1], **style)
        
        # 计算统计特性（使用原始数据）
        F_avg, F_rms, C_avg, C_rms = calculate_statistics(total_force)
        print(f"\n{mesh_type} 网格总力的统计结果:")
        print(f"力的平均值: {F_avg}")
        print(f"力的RMS值: {F_rms}")
        print(f"力系数平均值: {C_avg}")
        print(f"力系数RMS值: {C_rms}")
        
        # 进行FFT分析（使用原始数据）
        dt = time[1] - time[0]
        print(f"\n警告 - FFT分析要求时间步长恒定！当前时间步长: {dt}")
        
        # 对Fy进行FFT分析
        freq, var = FFT_analysis(total_force[:, 1], dt)
        ax_fft.semilogx(freq, var, **style)
    
    # 设置力图的标题和标签
    ax1.set_title('Force in x direction')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Force [N]')
    ax1.grid(True)
    ax1.legend()
    
    ax2.set_title('Force in y direction')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Force [N]')
    ax2.grid(True)
    ax2.legend()
    
    # 设置FFT图的标题和标签
    ax_fft.set_title('FFT Analysis of Forces')
    ax_fft.set_xlabel('Frequency [Hz]')
    ax_fft.set_ylabel('Variance [N]')
    ax_fft.grid(True)
    ax_fft.legend()
    
    # 调整布局并保存图片
    fig_forces.tight_layout()
    fig_fft.tight_layout()
    
    fig_forces.savefig('forces_comparison.png', dpi=300, bbox_inches='tight')
    fig_fft.savefig('fft_comparison.png', dpi=300, bbox_inches='tight')
    
    print("\n所有文件处理完成！")
    print("已保存对比图到: forces_comparison.png")
    print("已保存FFT对比图到: fft_comparison.png")
    
    # 关闭所有图形
    plt.close('all')

if __name__ == "__main__":
    main() 