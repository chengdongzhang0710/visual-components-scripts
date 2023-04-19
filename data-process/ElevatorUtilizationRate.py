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


def weight_utilization(rate, col, count):
    col_name = col.split(":")[0]
    agv_time = DISTANCE_MAP[col_name] / MOVE_SPEED  # 电梯负荷暂时不计算AGV装卸货时间和电梯装卸货时间
    busy_time = SIM_TIME * rate / 100 + agv_time * count
    return busy_time / SIM_TIME


def cal_utilization(df_loc, tb_loc):
    df = pd.read_csv(df_loc, index_col=0)
    tb = pd.read_csv(tb_loc, index_col=0)
    rates = np.array(df.iloc[-1])
    columns = df.columns
    counts = np.array(tb.iloc[-1])
    y = []
    for i in range(len(columns)):
        y.append(weight_utilization(rates[i], columns[i], counts[i]))
    return y


# data collect
labels = ["Factory #1", "Factory #3", "Factory #9"]

y1 = cal_utilization("Factory1EUR.csv", "Factory1ERT.csv")
y3 = cal_utilization("Factory3EUR.csv", "Factory3ERT.csv")
y9 = cal_utilization("Factory9EUR.csv", "Factory9ERT.csv")

# plot figure
width = 1
between = 2

x_start1 = 0
x_end1 = x_start1 + width * len(y1)
x_middle1 = (x_start1 + x_end1 - width) / 2
x1 = np.arange(x_start1, x_end1, width)

x_start3 = x_end1 + between
x_end3 = x_start3 + width * len(y3)
x_middle3 = (x_start3 + x_end3 - width) / 2
x3 = np.arange(x_start3, x_end3, width)

x_start9 = x_end3 + between
x_end9 = x_start9 + width * len(y9)
x_middle9 = (x_start9 + x_end9 - width) / 2
x9 = np.arange(x_start9, x_end9, width)

x_ticks = [x_middle1, x_middle3, x_middle9]

plt.figure(figsize=(18, 9))

plt.grid(axis="y")

plt.bar(x1, y1, width / 2, label=labels[0])
plt.bar(x3, y3, width / 2, label=labels[1])
plt.bar(x9, y9, width / 2, label=labels[2])

plt.title("Elevator Overall Utilization Rates")
plt.xlabel("Factory Category")
plt.ylabel("Utilization Rate")
plt.xticks(x_ticks, labels=labels)
plt.yticks(np.arange(0, 1.1, 0.1))
plt.ylim(0, 1)

plt.show()
