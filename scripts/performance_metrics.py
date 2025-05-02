import time
import psutil
import csv
import re
from pathlib import Path
import subprocess
from datetime import datetime

class PerformanceMetrics:
    def __init__(self, case_dir):
        self.case_dir = Path(case_dir)
        self.start_time = time.time()
        self.metrics = {
            'case_name': case_dir.name,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_time': 0,
            'gmsh_to_foam_time': 0,
            'decompose_par_time': 0,
            'solver_time': 0,
            'peak_memory_usage': 0,
            'cell_count': 0,
            'max_courant_number': 0,
            'avg_iterations_per_timestep': 0,
            'final_residuals': {},
        }
        
    def start_timer(self):
        self.timer_start = time.time()
        
    def stop_timer(self, metric_name):
        elapsed = time.time() - self.timer_start
        self.metrics[metric_name] = elapsed
        
    def get_cell_count(self):
        """从polyMesh/points文件获取网格单元数"""
        points_file = self.case_dir / 'constant' / 'polyMesh' / 'points'
        if points_file.exists():
            with open(points_file, 'r') as f:
                first_line = f.readline().strip()
                try:
                    self.metrics['cell_count'] = int(first_line)
                except ValueError:
                    pass
                    
    def parse_log_file(self):
        """解析log文件获取求解器性能指标"""
        log_file = list(self.case_dir.glob("log.mpiexec*"))[0]
        if not log_file.exists():
            return
            
        courant_numbers = []
        iterations = []
        final_residuals = {}
        
        with open(log_file, 'r') as f:
            for line in f:
                # 提取Courant数
                if "Courant Number mean" in line:
                    match = re.search(r"max: (\d+\.?\d*)", line)
                    if match:
                        courant_numbers.append(float(match.group(1)))
                
                # 提取迭代次数
                if "PIMPLE: iteration" in line:
                    iterations.append(1)
                    
                # 提取最终残差
                if "Final residual" in line:
                    for field in ["p", "U"]:
                        match = re.search(f"({field}), Initial residual = (\d+\.?\d*e?-?\d*)", line)
                        if match:
                            final_residuals[field] = float(match.group(2))
        
        if courant_numbers:
            self.metrics['max_courant_number'] = max(courant_numbers)
        if iterations:
            self.metrics['avg_iterations_per_timestep'] = sum(iterations) / len(iterations)
        self.metrics['final_residuals'] = final_residuals
        
    def get_memory_usage(self):
        """获取内存使用峰值"""
        self.metrics['peak_memory_usage'] = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
    def save_to_csv(self, csv_file='performance_metrics.csv'):
        """保存指标到CSV文件"""
        file_exists = Path(csv_file).exists()
        
        with open(csv_file, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.metrics.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(self.metrics)
            
    def collect_all_metrics(self):
        """收集所有性能指标"""
        self.get_cell_count()
        self.parse_log_file()
        self.get_memory_usage()
        self.metrics['total_time'] = time.time() - self.start_time 