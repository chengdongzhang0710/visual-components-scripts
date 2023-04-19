import numpy as np
import geatpy as ea
import time


# 采用带精英保留的遗传算法"Elitist Reservation GA"解决McCormick函数的最小化搜索问题


# 目标函数
def aim(Phen):
    x1 = Phen[:, [0]]
    x2 = Phen[:, [1]]
    return np.sin(x1 + x2) + (x1 - x2) ** 2 - 1.5 * x1 + 2.5 * x2 + 1


# 变量设置
x1 = [-1.5, 4]  # 决策变量范围
x2 = [-3, 4]

b1 = [1, 1]  # 决策变量边界，1表示包含范围的边界，0表示不包含
b2 = [1, 1]

ranges = np.vstack([x1, x2]).T
borders = np.vstack([b1, b2]).T

varTypes = np.array([0, 0])  # 决策变量的类型，0表示连续，1表示离散

# 染色体编码设置
Encoding = "BG"
codes = [1, 1]  # 决策变量的编码方式，两个1表示变量均使用格雷编码
precisions = [6, 6]  # 决策变量的编码精度，表示解码后能表示的决策变量精度可达到小数点后6位
scales = [0, 0]  # 0表示采用算术刻度，1表示采用对数刻度(废弃)

FieldD = ea.crtfld(Encoding, varTypes, ranges, borders, precisions, scales)  # 调用函数创建译码矩阵

# 遗传算法参数设置
NIND = 20  # 种群个体数目
MAXGEN = 100  # 最大遗传代数
maxormins = np.array([1])  # 表示目标函数是最小化，元素为-1则表示对应的目标函数是最大化
selectStyle = "sus"  # 选择 - 采用随机抽样选择
recStyle = "xovdp"  # 重组 - 采用两点交叉
mutStyle = "mutbin"  # 变异 - 采用二进制染色体的变异算子
LIND = int(np.sum(FieldD[0, :]))  # 计算染色体长度
pc = 0.9  # 交叉概率
pm = 1 / LIND  # 变异概率
obj_trace = np.zeros((MAXGEN, 2))  # 定义目标函数值记录器(均值和最优值)
var_trace = np.zeros((MAXGEN, LIND))  # 染色体记录器，记录历代最优个体的染色体

# 遗传算法进化
start_time = time.time()
Chrom = ea.crtpc(Encoding, NIND, FieldD)  # 生成种群染色体矩阵
variable = ea.bs2ri(Chrom, FieldD)  # 对初始种群进行解码
ObjV = aim(variable)  # 计算初始种群的目标函数值
best_ind = np.argmin(ObjV)  # 计算当代最优个体的序号

for gen in range(MAXGEN):
    FitnV = ea.ranking(maxormins * ObjV)  # 根据目标函数大小分配适应度值
    SelCh = Chrom[ea.selecting(selectStyle, FitnV, NIND - 1), :]  # 选择
    SelCh = ea.recombin(recStyle, SelCh, pc)  # 重组
    SelCh = ea.mutate(mutStyle, Encoding, SelCh, pm)  # 变异

    Chrom = np.vstack([Chrom[best_ind, :], SelCh])  # 把父代精英个体与子代的染色体进行合并，得到新一代种群
    Phen = ea.bs2ri(Chrom, FieldD)  # 对种群进行解码(二级制转十进制)
    ObjV = aim(Phen)  # 求种群个体的目标函数值

    best_ind = np.argmin(ObjV)  # 计算当代最优个体的序号
    obj_trace[gen, 0] = np.sum(ObjV) / ObjV.shape[0]  # 记录当代种群的目标函数均值
    obj_trace[gen, 1] = ObjV[best_ind]  # 记录当代种群最优个体目标函数值
    var_trace[gen, :] = Chrom[best_ind, :]  # 记录当代种群最优个体的染色体

end_time = time.time()
ea.trcplot(obj_trace, [["种群个体平均目标函数值", "种群最优个体目标函数值"]])

# 输出结果
best_gen = np.argmin(obj_trace[:, [1]])
print("最优解的目标函数值：", obj_trace[best_gen, 1])

variable = ea.bs2ri(var_trace[[best_gen], :], FieldD)  # 解码得到表现型，即对应的决策变量值
print("最优解的决策变量值为：")
for i in range(variable.shape[1]):
    print(f"x{i} = {variable[0, i]}")

print("用时：", end_time - start_time, "秒")
