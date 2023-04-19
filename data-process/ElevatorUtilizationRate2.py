import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as psl


# set global style
psl.use("seaborn-talk")


# util functions
DISTANCE_MAP = {
    "Elevator #1 #1": 19161,
    "Elevator #1 #2": 16573,
    "Elevator #1 #3": 11764,
    "Elevator #1 #4": 23966,
    "Elevator #1 #5": 21110,
    "Elevator #1 #6": 18270,
    "Elevator #1 #7 New": 14041,
    "Elevator #1 #8 New": 11095,
    "Elevator #1 #9 New": 13478,
    "Elevator #1 #10 New": 7932,
    "Elevator #3 #1": 27592,
    "Elevator #3 #2": 24656,
    "Elevator #3 #3": 21776,
    "Elevator #3 #4": 15876,
    "Elevator #3 #5": 13060,
    "Elevator #3 #6": 10378,
    "Elevator #9 #3": 8518,
    "Elevator #9 #4": 18357,
    "Elevator #9 #5": 11293,
    "Elevator #9 #6": 10599,
    "Elevator #9 #7": 10818,
    "Elevator #9 #8": 10607,
}  # Process Node原点到原点，实际距离会比计算短
SIM_TIME = 11 * 3600
MOVE_SPEED = 1000
# AGV_PROCESS_TIME = 5
# ELEVATOR_PROCESS_TIME = 15


def weight_utilization(distance, rate, count):
    agv_time = distance / MOVE_SPEED  # 电梯负荷暂时不计算AGV装卸货时间和电梯装卸货时间
    busy_time = SIM_TIME * rate / 100 + agv_time * count
    return busy_time / SIM_TIME


def cal_utilization(df, tb, sub_col):
    y = []
    for i in range(len(sub_col)):
        sub_y = []
        for col in sub_col[i]:
            distance = DISTANCE_MAP[col]
            rate = df[col].iloc[-1]
            count = tb[col].iloc[-1]
            sub_y.append(weight_utilization(distance, rate, count))
        y.append(sub_y)
    return y


# data collect
labels = []

# Factory #1
df1 = pd.read_csv("Factory1EUR.csv", index_col=0)
tb1 = pd.read_csv("Factory1ERT.csv", index_col=0)
cols1 = list(map(lambda s: s.split(":")[0], df1.columns))
df1.columns = cols1
tb1.columns = cols1

sub_cols1 = [
    ["Elevator #1 #3"],
    ["Elevator #1 #4", "Elevator #1 #5", "Elevator #1 #6", "Elevator #1 #7 New", "Elevator #1 #8 New"],
    ["Elevator #1 #1", "Elevator #1 #2", "Elevator #1 #9 New"],
]
labels.extend(["#1 Up", "#1 Right", "#1 Left"])

y1 = cal_utilization(df1, tb1, sub_cols1)

# Factory #3
df3 = pd.read_csv("Factory3EUR.csv", index_col=0)
tb3 = pd.read_csv("Factory3ERT.csv", index_col=0)
cols3 = list(map(lambda s: s.split(":")[0], df3.columns))
df3.columns = cols3
tb3.columns = cols3

sub_cols3 = [
    ["Elevator #3 #1", "Elevator #3 #2", "Elevator #3 #3", "Elevator #3 #4", "Elevator #3 #5", "Elevator #3 #6"]
]
labels.extend(["#3"])

y3 = cal_utilization(df3, tb3, sub_cols3)

# Factory #9
df9 = pd.read_csv("Factory9EUR.csv", index_col=0)
tb9 = pd.read_csv("Factory9ERT.csv", index_col=0)
cols9 = list(map(lambda s: s.split(":")[0], df9.columns))
df9.columns = cols9
tb9.columns = cols9

sub_cols9 = [
    ["Elevator #9 #7", "Elevator #9 #8"],
    ["Elevator #9 #5", "Elevator #9 #6"],
    ["Elevator #9 #3", "Elevator #9 #4"],
]
labels.extend(["#9 Right", "#9 Left", "#9 Down"])

y9 = cal_utilization(df9, tb9, sub_cols9)


# plot figure
width = 1

plt.figure(figsize=(18, 9))

plt.grid(axis="y")

x_end = -width
x_ticks = []
idx = 0
for y in [y1, y3, y9]:
    for sub_y in y:
        x_start = x_end + width
        x_end = x_start + width * len(sub_y)
        x_middle = (x_start + x_end - width) / 2
        x_ticks.append(x_middle)
        x = np.arange(x_start, x_end, width)

        plt.bar(x, np.array(sub_y), width / 2, label=labels[idx])
        idx += 1
    x_end += 3 * width

plt.title("Elevator Overall Utilization Rates")
plt.xlabel("Factory Area")
plt.ylabel("Utilization Rate")
plt.xticks(x_ticks, labels=labels)
plt.yticks(np.arange(0, 1.1, 0.1))
plt.ylim(0, 1)

plt.show()
