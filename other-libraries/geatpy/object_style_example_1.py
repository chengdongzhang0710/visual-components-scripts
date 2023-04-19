import numpy as np
import geatpy as ea


# 采用差分进化算法"DE/best/1/L"求解带不等式约束和等式约束的单目标最大化优化问题


class MyProblem(ea.Problem):
    def __init__(self):
        name = "MyProblem"  # 初始化函数名称，可以随意设置
        M = 1  # 初始化目标维数
        maxormins = [-1]  # 初始化目标最小最大化标记列表
        Dim = 3  # 初始化决策变量维数
        varTypes = [0] * Dim  # 初始化决策变量类型
        lb = [0, 0, 0]  # 决策变量下界
        ub = [1, 1, 2]  # 决策变量上界
        lbin = [1, 1, 0]  # 决策变量下边界
        ubin = [1, 1, 0]  # 决策变量上边界

        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)

    def aimFunc(self, pop):
        Vars = pop.Phen  # 得到决策变量矩阵
        x1 = Vars[:, [0]]
        x2 = Vars[:, [1]]
        x3 = Vars[:, [2]]
        pop.ObjV = 4 * x1 + 2 * x2 + x3  # 计算目标函数值，赋值给pop种群对象的ObjV属性
        pop.CV = np.hstack([2 * x1 + x2 - 1, x1 + 2 * x3 - 2, np.abs(x1 + x2 + x3 - 1)])  # 采用可行性法则处理约束，生成种群个体违反约束程度矩阵

    # 采用罚函数法处理约束
    # 本案例中包含一个等式约束，用这种简单的惩罚方式难以找到可行解
    # def aimFunc(self, pop):
    #     Vars = pop.Phen  # 得到决策变量矩阵
    #     x1 = Vars[:, [0]]
    #     x2 = Vars[:, [1]]
    #     x3 = Vars[:, [2]]
    #     f = 4 * x1 + 2 * x2 + x3
    #
    #     exIdx1 = np.where(2 * x1 + x2 > 1)[0]  # 找到违反约束条件的个体索引
    #     exIdx2 = np.where(x1 + 2 * x3 > 2)[0]
    #     exIdx3 = np.where(x1 + x2 + x3 != 1)[0]
    #     exIdx = np.unique(np.hstack([exIdx1, exIdx2, exIdx3]))  # 合并索引
    #
    #     alpha = 2  # 惩罚缩放因子
    #     beta = 1  # 惩罚最小偏移量
    #     f[exIdx] += self.maxormins[0] * alpha * (np.max(f) - np.min(f) + beta)
    #     pop.ObjV = f  # 把目标函数值矩阵赋值给种群的ObjV属性


if __name__ == "__main__":
    # 实例化问题对象
    problem = MyProblem()

    # 种群设置
    Encoding = "RI"  # 编码方式
    NIND = 50  # 种群规模
    Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders)  # 创建区域描述器
    population = ea.Population(Encoding, Field, NIND)

    # 算法参数设置
    myAlgorithm = ea.soea_DE_best_1_L_templet(problem, population)
    myAlgorithm.MAXGEN = 1000  # 最大进化代数
    myAlgorithm.mutOper.F = 0.5  # 差分进化中的参数F
    myAlgorithm.recOper.XOVR = 0.7  # 设置交叉概率
    myAlgorithm.logTras = 0  # 设置每个多少代记录日志，若设置成0则表示不记录日志
    myAlgorithm.verbose = True  # 设置是否打印输出日志信息
    myAlgorithm.drawing = 1  # 设置绘图方式，0 - 不绘图，1 - 绘制结果图，2 - 绘制目标空间过程动画，3 - 绘制决策空间过程动画

    # 调用算法模板进行种群进化
    [BestIndi, population] = myAlgorithm.run()  # 执行算法模板，得到最优个体以及最后一代种群
    BestIndi.save()  # 把最优个体的信息保存到文件中

    # 输出结果
    print(f"评价次数：{myAlgorithm.evalsNum}")
    print(f"时间：{myAlgorithm.passTime}")

    if BestIndi.sizes != 0:
        print(f"最优的目标函数值为：{BestIndi.ObjV[0][0]}")
        print("最优的控制变量值为：")
        for i in range(BestIndi.Phen.shape[1]):
            print(BestIndi.Phen[0, i])
    else:
        print("没有找到可行解")
