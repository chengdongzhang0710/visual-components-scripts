import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as psl


# set global style
psl.use("seaborn-talk")


# data collect
labels = ["Factory #1", "Factory #3", "Factory #9"]

df1 = pd.read_csv("Factory1PAUR.csv", index_col=0)
y1 = np.array(df1.iloc[-1])

df3 = pd.read_csv("Factory3PAUR.csv", index_col=0)
y3 = np.array(df3.iloc[-1])

df9 = pd.read_csv("Factory9PAUR.csv", index_col=0)
y9 = np.array(df9.iloc[-1])


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

plt.title("Parking Area Overall Utilization Rates")
plt.xlabel("Factory Category")
plt.ylabel("Utilization Rate")
plt.xticks(x_ticks, labels=labels)
plt.yticks(np.arange(0, 1.1, 0.1))

plt.show()
