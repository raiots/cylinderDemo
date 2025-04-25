import foamlib
from foamlib import FoamCase
from pathlib import Path
import shutil
import re

case = FoamCase(Path("sim/simple_cylinder"))

# 如果存在pimple_cylinder文件夹，则删除
if Path("sim/pimple_cylinder").exists():
    shutil.rmtree(Path("sim/pimple_cylinder"))

case.clean()
case.run("decomposePar")
case.run("simpleFoam")
case.copy(Path("sim/pimple_cylinder"))

# 删除目标文件夹中的0文件夹
target_zero = Path("sim/pimple_cylinder") / "0"
if target_zero.exists():
    shutil.rmtree(target_zero)

# 找到最大数字文件夹并重命名为0
target_dir = Path("sim/pimple_cylinder")
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


case = FoamCase(Path("sim/pimple_cylinder"))
case.clean()
case.fv_schemes["ddtSchemes"]["default"] = "backward"
case.control_dict["application"] = "pimpleFoam"
case.control_dict["endTime"] = 5.0
case.control_dict["deltaT"] = 1e-3
case.decompose_par_dict["numberOfSubdomains"] = 8
case.run("decomposePar")
case.run("mpiexec -np 8 pimpleFoam -parallel")


