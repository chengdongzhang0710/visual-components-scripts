import numpy as np
import geatpy as ea


class MyProblem(ea.Problem):
    def __init__(self):
        name = "MyProblem"
        M = 1
        maxormins = [-1]
        Dim = 1
        varTypes = [0] * Dim
        lb = [-1]
        ub = [2]
        lbin = [1] * Dim
        ubin = [1] * Dim

        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)

    def aimFunc(self, pop):
        Var = pop.Phen
        x = Var[:, [0]]
        pop.ObjV = x * np.sin(10 * np.pi * x) + 2.0


if __name__ == "__main__":
    problem = MyProblem()

    Encoding = "RI"
    NINDs = [5, 10, 15, 20]
    population = []
    for i in range(len(NINDs)):
        Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders)
        population.append(ea.Population(Encoding, Field, NINDs[i]))

    myAlgorithm = ea.soea_multi_SEGA_templet(problem, population)
    myAlgorithm.MAXGEN = 50
    myAlgorithm.trappedValue = 1e-6  # “进化停滞”判断阈值
    myAlgorithm.maxTrappedCount = 5  # 进化停滞计数器最大上限值，如果连续maxTrappedCount代被判定进化陷入停滞，则终止进化

    [best_indi, pop] = myAlgorithm.run()
    best_indi.save()

    print(f"最优的目标函数值为：{best_indi.ObjV[0][0]}")
    print("最优的控制变量值为：")
    for i in range(best_indi.Phen.shape[1]):
        print(best_indi.Phen[0, i])
    print(f"评价次数：{myAlgorithm.evalsNum}")
    print(f"时间已过{myAlgorithm.passTime}秒")
