import foamlib
from foamlib import FoamCase
from pathlib import Path
import shutil
import re
import numpy as np

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

def get_yplus_average(case_dir):
    """获取最后时间步的y+平均值"""
    yplus_dir = case_dir / "postProcessing" / "yPlus" / "0"
    if not yplus_dir.exists():
        return None
    
    # 获取最后一个yPlus数据文件
    yplus_files = list(yplus_dir.glob("yPlus_*.dat"))
    if not yplus_files:
        return None
    
    latest_file = yplus_files[-1]
    with open(latest_file, 'r') as f:
        lines = f.readlines()
        if len(lines) < 3:  # 确保文件有足够的行数
            return None
        # 获取最后一行的平均值（第5列）
        last_line = lines[-1].strip().split()
        return float(last_line[4])

def main():
    # 获取所有.msh文件
    source_dir = Path("sim/simple_cylinder")
    msh_files = list(source_dir.glob("*.msh"))
    results = {}

    # 为每个.msh文件创建一个任务
    for msh_file in msh_files:
        print(f"\n处理网格文件: {msh_file.name}")
        
        # 设置初始case
        case = FoamCase(source_dir)
        case.clean()
        
        # 删除 polyMesh 文件夹
        polyMesh_dir = source_dir / "constant" / "polyMesh"
        if polyMesh_dir.exists():
            shutil.rmtree(polyMesh_dir)
        
        # 转换网格
        print("转换GMSH网格...")
        case.run(f"gmshToFoam {msh_file.name}")
        case.run("transformPoints -scale '(0.0405 0.0405 0.0405)'")
        
        # 修改 boundary 文件
        modify_boundary_file(source_dir)
        
        # 运行simpleFoam
        print("运行simpleFoam...")
        case.run("simpleFoam")
        
        # 获取y+值
        yplus_avg = get_yplus_average(source_dir)
        if yplus_avg is not None:
            results[msh_file.name] = yplus_avg
        
        print(f"完成 {msh_file.name} 的处理")

    # 打印结果
    print("\n各网格的y+平均值:")
    print("-" * 40)
    print("网格文件名称".ljust(30), "y+平均值")
    print("-" * 40)
    for mesh_name, yplus in results.items():
        print(f"{mesh_name:<30} {yplus:.6f}")

if __name__ == "__main__":
    main() 