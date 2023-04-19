import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime


# util functions
def df_process(df):
    df.drop("Simulation Time", axis=1, inplace=True)
    col_num = len(df.columns)
    df["Total Count"] = df.apply(lambda n: n.sum(), axis=1)
    df["Utilization Rate"] = df["Total Count"].apply(lambda n: n / col_num)
    y = np.array(df["Utilization Rate"])
    return y


# data collect
labels = ["Factory #1", "Factory #3", "Factory #9"]

df1 = pd.read_csv("Factory1ENC.csv")
y1 = df_process(df1)

df3 = pd.read_csv("Factory3ENC.csv")
y3 = df_process(df3)

df9 = pd.read_csv("Factory9ENC.csv")
y9 = df_process(df9)

# plot figure
x = []
start = datetime.datetime(2022, 3, 1, 8, 0)
for i in range(len(y1)):
    now = start + datetime.timedelta(minutes=i)
    x.append(now.strftime("%H:%M"))

plt.figure(figsize=(18, 5))

plt.suptitle("Elevator Category Utilization Rate vs Time", fontsize=16)

x_ticks = np.arange(0, len(x), 120)
y_ticks = np.arange(0, 1.1, 0.1)

axis1 = plt.subplot(131, title=labels[0], xlabel="Time", ylabel="Utilization Rate", xticks=x_ticks, yticks=y_ticks,
                    ylim=(0, 1))
axis1.plot(x, y1)
axis1.grid(axis="y")

axis3 = plt.subplot(132, title=labels[1], xlabel="Time", ylabel="Utilization Rate", xticks=x_ticks, yticks=y_ticks,
                    ylim=(0, 1))
axis3.plot(x, y3)
axis3.grid(axis="y")

axis9 = plt.subplot(133, title=labels[2], xlabel="Time", ylabel="Utilization Rate", xticks=x_ticks, yticks=y_ticks,
                    ylim=(0, 1))
axis9.plot(x, y9)
axis9.grid(axis="y")

plt.show()
