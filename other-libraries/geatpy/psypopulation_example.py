import numpy as np
import geatpy as ea


class MyProblem(ea.Problem):
    def __init__(self):
        name = "MyProblem"
        M = 1
        maxormins = [-1]
        Dim = 6
        varTypes = [0, 0, 1, 1, 1, 1]
        lb = [-1.5, -1.5, 1, 1, 1, 1]
        ub = [2.5, 2.5, 7, 7, 7, 7]
        lbin = [1] * Dim
        ubin = [1] * Dim

        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)

    def aimFunc(self, pop):
        X = pop.Phen
        x1 = X[:, [0]]
        x2 = X[:, [1]]
        x3 = X[:, [2]]
        x4 = X[:, [3]]
        x5 = X[:, [4]]
        x6 = X[:, [5]]
        pop.ObjV = np.sin(2 * x1) - np.cos(x2) + 2 * x3 ** 2 - 3 * x4 + (x5 - 3) ** 2 + 7 * x6


if __name__ == "__main__":
    # 实例化问题对象
    problem = MyProblem()

    # 种群设置
    NIND = 40
    Encodings = ["RI", "P"]
    Field1 = ea.crtfld(Encodings[0], problem.varTypes[:2], problem.ranges[:, :2], problem.borders[:, :2])
    Field2 = ea.crtfld(Encodings[1], problem.varTypes[2:], problem.ranges[:, 2:], problem.borders[:, 2:])
    Fields = [Field1, Field2]
    population = ea.PsyPopulation(Encodings, Fields, NIND)

    # 算法参数设置
    myAlgorithm = ea.soea_psy_EGA_templet(problem, population)
    myAlgorithm.MAXGEN = 25
    myAlgorithm.logTras = 1
    myAlgorithm.verbose = True
    myAlgorithm.drawing = 1
    [BestIndi, population] = myAlgorithm.run()  # 执行算法模板，得到最优个体以及最后一代种群
    BestIndi.save()

    # 输出结果
    print(f"评价次数：{myAlgorithm.evalsNum}")
    print(f"时间已过{myAlgorithm.passTime}秒")
    if BestIndi.sizes != 0:
        print(f"最优的目标函数值为：{BestIndi.ObjV[0][0]}")
        print("最优的控制变量值为：")
        for i in range(BestIndi.Phen.shape[1]):
            print(BestIndi.Phen[0, i])
    else:
        print("没有找到可行解")
