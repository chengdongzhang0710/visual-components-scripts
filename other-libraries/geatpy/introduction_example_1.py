import numpy as np
import geatpy as ea


# 构建问题
# @ea.Problem.single
# def evalVars(Vars):
#     f = np.sum((Vars - 1)**2)  # 目标函数

#     x1 = Vars[0]
#     x2 = Vars[1]
#     CV = np.array([(x1 - 0.5)**2 - 0.25, (x2 - 1)**2 - 1])  # 违反约束程度

#     return f, CV


# 在定义目标函数时不加ea.Problem.single标记
# 传入目标函数evalVars()的参数Vars是一个Numpy ndarray二维数组，它是NIND行Dim列：NIND是种群的个体数，即种群规模；Dim是自定义的问题的决策变量个数
# 函数返回的ObjV是一个NIND行1列的Numpy ndarray二维数组，CV是一个NIND行2列的Numpy ndarray二维数组
def evalVars(Vars):
    ObjV = np.sum((Vars - 1) ** 2, 1, keepdims=True)

    x1 = Vars[:, [0]]
    x2 = Vars[:, [1]]
    CV = np.hstack([(x1 - 0.5) ** 2 - 0.25, (x2 - 1) ** 2 - 1])

    return ObjV, CV


problem = ea.Problem(
    name="soea quick start demo",
    M=1,  # 目标函数维度
    maxormins=[1],  # 目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标
    Dim=5,  # 决策变量维数
    varTypes=[0, 0, 1, 1, 1],  # 决策变量的类型列表，0：实数；1：整数
    lb=[-1, 1, 2, 1, 0],  # 决策变量下界
    ub=[1, 4, 5, 2, 1],  # 决策变量上界
    evalVars=evalVars,
)

# 构建算法
algorithm = ea.soea_SEGA_templet(
    problem=problem,
    population=ea.Population(Encoding="RI", NIND=20),
    MAXGEN=50,  # 最大进化代数
    logTras=1,  # 表示每隔多少代记录一次日志信息，0表示不记录
    trappedValue=1e-6,  # 单目标优化陷入停滞的判断阈值
    maxTrappedCount=10,  # 进化停滞计数器最大上限值
)

# 求解
res = ea.optimize(algorithm=algorithm, seed=1, verbose=True, drawing=1, outputMsg=True, drawLog=False,
                  dirName="result_1")
