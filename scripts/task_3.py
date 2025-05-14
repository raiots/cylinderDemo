'''
Wall modeled
'''

import foamlib
from foamlib import FoamCase
from pathlib import Path
import shutil
import re
import glob
from performance_metrics import PerformanceMetrics

def modify_boundary_file(case_dir):
    """修改 boundary 文件中的边界类型"""
    boundary_file = case_dir / "constant" / "polyMesh" / "boundary"
    
    with open(boundary_file, 'r') as f:
        content = f.read()
    
    # 修改 sides 的类型
    content = re.sub(r'(sides\s*{[^}]*type\s+)patch(.*?physicalType\s+)patch', r'\1empty\2empty', content, flags=re.DOTALL)
    
    # 修改 wall 的类型
    content = re.sub(r'(wall\s*{[^}]*type\s+)patch(.*?physicalType\s+)patch', r'\1wall\2wall', content, flags=re.DOTALL)
    
    with open(boundary_file, 'w') as f:
        f.write(content)

# 定义要测试的CFL值
cfl_values = [1, 5, 20, 50]
base_deltaT = 1e-3  # 基准deltaT值，对应CFL=23
base_cfl = 23       # 基准CFL值

# 使用模板网格文件
template_msh = Path("sim/simple_cylinder_wall_modeled/2D_Cylinder_Template.msh")

# 为每个CFL值创建一个任务
for cfl in cfl_values:
    # 计算对应的deltaT
    deltaT = (base_deltaT * cfl) / base_cfl
    task_name = f"task_cfl_{cfl}"
    source_dir = Path("sim/simple_cylinder_wall_modeled")
    target_dir = Path("sim") / task_name
    
    print(f"Processing CFL={cfl} -> {task_name}")
    
    # 初始化性能指标收集器
    metrics = PerformanceMetrics(target_dir)
    
    # 设置初始case
    case = FoamCase(source_dir)
    case.clean()
    # 删除 polyMesh 文件夹
    polyMesh_dir = source_dir / "constant" / "polyMesh"
    if polyMesh_dir.exists():
        shutil.rmtree(polyMesh_dir)
    
    # 记录gmshToFoam时间
    metrics.start_timer()
    case.run(f"gmshToFoam {template_msh.name}")
    metrics.stop_timer('gmsh_to_foam_time')

    case.run("transformPoints -scale '(0.0405 0.0405 0.0405)'")
    
    # 修改 boundary 文件
    modify_boundary_file(source_dir)
    
    # 记录simpleFoam求解时间
    metrics.start_timer()
    case.run("simpleFoam")
    metrics.stop_timer('solver_time')
    
    # 复制到新的任务目录
    if not target_dir.exists():
        case.copy(target_dir)
    
    # 删除目标文件夹中的0文件夹
    target_zero = target_dir / "0"
    if target_zero.exists():
        shutil.rmtree(target_zero)
    
    # 找到最大数字文件夹并重命名为0
    time_dirs = []
    for d in target_dir.iterdir():
        if d.is_dir() and d.name.isdigit():
            time_dirs.append(int(d.name))
    
    # 如果存在时间文件夹，则找到最大时间文件夹并重命名为0
    if time_dirs:
        max_time = max(time_dirs)
        max_dir = target_dir / str(max_time)
        new_dir = target_dir / "0"
        max_dir.rename(new_dir)
    
    # 设置pimpleFoam配置
    case = FoamCase(target_dir)
    case.clean()
    case.fv_schemes["ddtSchemes"]["default"] = "backward"
    case.control_dict["application"] = "pimpleFoam"
    case.control_dict["endTime"] = 5.0
    case.control_dict["deltaT"] = deltaT  # 使用计算得到的deltaT
    case.decompose_par_dict["numberOfSubdomains"] = 4

    case.run("checkMesh")

    # 记录decomposePar时间
    metrics.start_timer()
    case.run("decomposePar")
    metrics.stop_timer('decompose_par_time')
    
    # 记录pimpleFoam求解时间
    metrics.start_timer()
    case.run("mpiexec -np 4 pimpleFoam -parallel")
    metrics.stop_timer('solver_time')
    
    # 收集并保存所有性能指标
    metrics.collect_all_metrics()
    metrics.save_to_csv()
    
    print(f"Completed {task_name}") 