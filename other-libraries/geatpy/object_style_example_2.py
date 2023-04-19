import numpy as np
import geatpy as ea


# 带约束的多目标优化问题


# Geatpy的问题类有三大函数：构造函数__init__()、目标函数aimFunc()以及计算理论参考解的目标函数参考值(常常是理论最优解)的函数calReferObjV()
# 如果实际问题并不知道模型的理论最优解的目标函数参考值，那么calReferObjV()函数的定义可以被忽略
# 在多目标优化中，“真实帕累托前沿”可在calReferObjV()中进行计算或者读取文件得到
class MyProblem(ea.Problem):
    def __init__(self):
        name = "BNH"  # 初始化函数名称
        M = 2  # 初始化目标维数
        maxormins = [1] * M  # 初始化目标最小最大化标记列表
        Dim = 2  # 初始化决策变量维数
        varTypes = [0] * Dim  # 初始化决策变量类型
        lb = [0, 0]  # 决策变量下界
        ub = [5, 3]  # 决策变量上界
        lbin = [1] * Dim  # 决策变量下边界
        ubin = [1] * Dim  # 决策变量上边界

        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)

    def aimFunc(self, pop):
        Vars = pop.Phen
        x1 = Vars[:, [0]]
        x2 = Vars[:, [1]]
        f1 = 4 * x1 ** 2 + 4 * x2 ** 2
        f2 = 4 * (x1 - 5) ** 2 + 4 * (x2 - 5) ** 2
        pop.ObjV = np.hstack([f1, f2])
        pop.CV = np.hstack([(x1 - 5) ** 2 + x2 ** 2 - 25, -(x1 - 8) ** 2 - (x2 - 3) ** 2 + 7.7])

    # 计算全局最优解
    def calReferObjV(self):
        N = 10000
        x1 = np.linspace(0, 5, N)
        x2 = x1.copy()
        x2[x1 >= 3] = 3
        return np.vstack([4 * x1 ** 2 + 4 * x2 ** 2, 4 * (x1 - 5) ** 2 + 4 * (x2 - 5) ** 2]).T


if __name__ == "__main__":
    # 实例化问题对象
    problem = MyProblem()

    # 种群设置
    Encoding = "RI"  # 编码方式
    NIND = 100  # 种群规模
    Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders)  # 创建区域描述器
    population = ea.Population(Encoding, Field, NIND)

    # 算法参数设置
    myAlgorithm = ea.moea_NSGA2_templet(problem, population)
    myAlgorithm.mutOper.Pm = 0.2  # 修改变异算子的变异概率
    myAlgorithm.recOper.XOVR = 0.9  # 修改交叉算子的交叉概率
    myAlgorithm.MAXGEN = 200  # 最大进化代数
    myAlgorithm.logTras = 1  # 设置每多少代记录日志
    myAlgorithm.verbose = False  # 设置是否打印输出日志信息
    myAlgorithm.drawing = 1  # 设置绘图方式

    # 调用算法模板进行种群进化
    # 调用run执行算法模板，得到帕累托最优解集NDSet以及最后一代种群
    # NDSet是一个种群类Population的对象
    # NDSet.ObjV为最优解个体的目标函数值，NDSet.Phen为对应的决策变量值
    [NDSet, population] = myAlgorithm.run()  # 执行算法模板，得到非支配种群以及最后一代种群
    NDSet.save()  # 把非支配种群的信息保存到文件中

    # 输出结果
    print(f"用时：{myAlgorithm.passTime}")
    print(f"非支配个体数：{NDSet.sizes}个")

    if myAlgorithm.log is not None and NDSet.sizes != 0:
        print("GD", myAlgorithm.log["gd"][-1])
        print("IGD", myAlgorithm.log["igd"][-1])
        print("HV", myAlgorithm.log["hv"][-1])
        print("Spacing", myAlgorithm.log["spacing"][-1])

    # 进化过程指标追踪分析
    metricName = [["igd"], ["hv"]]
    Metrics = np.array([myAlgorithm.log[metricName[i][0]] for i in range(len(metricName))]).T
    ea.trcplot(Metrics, labels=metricName, titles=metricName)  # 绘制指标追踪分析图
