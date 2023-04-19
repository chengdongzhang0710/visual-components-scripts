import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as psl

# set global style
psl.use("seaborn-talk")


# util functions
def cal_wait_time(data):
    wait_in = []
    wait_out = []
    for i in range(1, len(data)):
        if data[i] > data[i - 1]:
            for _ in range(data[i] - data[i - 1]):
                wait_in.append(i)
        elif data[i] < data[i - 1]:
            for _ in range(data[i - 1] - data[i]):
                wait_out.append(i)

    if len(wait_in) != len(wait_out):
        raise Exception("Flow balance is not satisfied!")

    wait = []
    for i in range(len(wait_out)):
        wait.append(wait_out[i] - wait_in[i])

    return wait


# data collect
df = pd.read_csv("ElevatorAreaBufferCount.csv", index_col=0)
df.columns = ["Factory #1 Up", "Factory #1 Right", "Factory #1 Left", "Factory #3", "Factory #9 Right",
              "Factory #9 Left", "Factory #9 Down"]

labels = ["Factory #1 Up", "Factory #1 Left", "Factory #1 Right"]
y = []
for col in labels:
    wait_time = np.array(cal_wait_time(np.array(df[col])))
    y.append(wait_time.mean())

print("Waiting Time Results:", y)


# plot figure
plt.figure(figsize=(9, 9))

plt.grid(axis="y")

width = 1
x = np.arange(0, 5 * width * len(y), 5 * width)
plt.bar(x, y, width)

plt.title("Elevator Area Average Waiting Time")
plt.xlabel("Factory Area")
plt.ylabel("Waiting Time")
plt.xticks(x, labels=labels)
plt.yticks(np.arange(0, 61, 5))
plt.ylim(0, 60)

plt.show()
