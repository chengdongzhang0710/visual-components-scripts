import numpy as np
import geatpy as ea


# 使用NSGA2算法求解双目标优化问题
class MyProblem(ea.Problem):
    def __init__(self):
        name = "MyProblem"
        M = 2  # 优化目标个数
        maxormins = [1] * M  # 初始化目标最小最大化标记列表(1 - 最小化该目标；-1 - 最大化该目标)
        Dim = 1  # 初始化决策变量维数
        varTypes = [0]  # 初始化决策变量类型(0 - 实数；1 - 整数)
        lb = [-10]  # 决策变量下界
        ub = [10]  # 决策变量上界
        lbin = [1]  # 决策变量下边界(0表示不包含该变量的下边界；1表示包含)
        ubin = [1]  # 决策变量上边界(0表示不包含该变量的下边界；1表示包含)

        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)

    # 目标函数
    # def evalVars(self, Vars):
    #     f1 = Vars**2
    #     f2 = (Vars - 2)**2
    #     ObjV = np.hstack([f1, f2])  # 计算目标函数值矩阵
    #     CV = -Vars**2 + 2.5 * Vars - 1.5  # 构建违反约束程度矩阵
    #     return ObjV, CV

    # aimFunc()写法，它传入一个种群对象，且不需要返回值
    def aimFunc(self, pop):
        Vars = pop.Phen
        f1 = Vars ** 2
        f2 = (Vars - 2) ** 2
        pop.ObjV = np.hstack([f1, f2])
        pop.CV = -Vars ** 2 + 2.5 * Vars - 1.5


if __name__ == "__main__":
    # 实例化问题对象
    problem = MyProblem()

    # 构建算法
    algorithm = ea.moea_NSGA2_templet(problem, ea.Population(Encoding="RI", NIND=50), MAXGEN=200, logTras=0)

    # 求解
    res = ea.optimize(algorithm, seed=1, verbose=False, drawing=1, outputMsg=True, drawLog=False, saveFlag=False,
                      dirName="result_2")
