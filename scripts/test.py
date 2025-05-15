#!/usr/bin/env python3
import foamlib
import os

def clean_case(case_path):
    """
    清理 OpenFOAM 案例目录
    """
    # 初始化 foamlib
    foam = foamlib.FoamCase(case_path)
    
    foam.clean()
    
    print(f"已清理案例目录: {case_path}")

if __name__ == "__main__":
    case_path = "sim/simple_cylinder_wall_modeled"
    clean_case(case_path)
