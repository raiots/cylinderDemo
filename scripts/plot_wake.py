import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 清除所有图形
plt.close('all')

# 加载数据
file_CFD = 'sim/task_cfl_20/wake.csv'
data_CFD = pd.read_csv(file_CFD)

# 提取数据
x = data_CFD['Points_0']
y = data_CFD['Points_1']
U_avg = data_CFD[['UMean_0', 'UMean_1', 'UMean_2']].values / 26.8
U_rms = np.sqrt(data_CFD[['UPrime2Mean_0', 'UPrime2Mean_1', 'UPrime2Mean_2', 
                         'UPrime2Mean_3', 'UPrime2Mean_4', 'UPrime2Mean_5']].values) / 26.8

# 计算速度大小
U_mag = np.sqrt(np.sum(U_avg**2, axis=1))

# 创建图形
plt.figure(figsize=(15, 5))

# 数据位置图
plt.subplot(131)
plt.plot(x, y, '.')
plt.title('Data location')
plt.xlabel('x [m]')
plt.ylabel('y [m]')
plt.legend(['OpenFOAM'])
plt.axis('equal')
plt.grid(True)

# 湍流强度图
plt.subplot(132)
plt.plot(U_rms[:, 0], y, '-r', label='$I_{xx}$')
plt.plot(U_rms[:, 1], y, '-b', label='$I_{yy}$')
plt.plot(U_rms[:, 2], y, '-k', label='$I_{zz}$')
plt.title('Resolved Turbulent intensity')
plt.xlabel('$I$')
plt.ylabel('$y$ [m]')
plt.legend()
plt.grid(True)

# 平均速度图
plt.subplot(133)
plt.plot(U_avg[:, 0], y, '-r', label='$u$')
plt.plot(U_avg[:, 1], y, '-b', label='$v$')
plt.plot(U_avg[:, 2], y, '-k', label='$w$')
plt.plot(U_mag, y, '-g', label='$|U|$')
plt.title('Avg. Velocity')
plt.xlabel('$\\overline{U}$')
plt.ylabel('$y$ [m]')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show() 