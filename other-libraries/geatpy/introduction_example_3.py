import numpy as np
import geatpy as ea

# 调用内置的benchmark测试问题

# 生成问题对象
problem = ea.benchmarks.DTLZ1()

# 构建算法
algorithm = ea.moea_NSGA3_templet(problem, ea.Population(Encoding="RI", NIND=100), MAXGEN=500, logTras=0)

# 求解
res = ea.optimize(algorithm, verbose=True, drawing=1, outputMsg=True, drawLog=True, saveFlag=True, dirName="result_3")
