import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as psl


# set global style
psl.use("seaborn-talk")


# util functions
def wait_time_calculation(data):
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
df = pd.read_csv("WaitingVehicleNumberCount.csv")
columns = df.columns[1:]
wait_time = np.array([])
for column in columns:
    temp = np.array(df[column])
    res = wait_time_calculation(temp)
    wait_time = np.append(wait_time, np.array(res))

wait_time.sort()

intervals = []
for num in range(13):
    intervals.append((num * 5, (num + 1) * 5))

y = np.array([0 for _ in range(len(intervals))])
current_idx = 0
current_interval = intervals[current_idx]
for t in wait_time:
    while not current_interval[0] <= t < current_interval[1]:
        current_idx += 1
        current_interval = intervals[current_idx]
    y[current_idx] += 1


# plot figure
width = 0.25
x = np.arange(width / 2, width / 2 + len(intervals) * width, width)

plt.figure(figsize=(12, 8))

plt.grid(axis="y")

plt.bar(x, y, width, edgecolor="black", linewidth=0.75)

plt.title("Waiting Time for Vehicles")
plt.xlabel("Time Interval / min")
plt.ylabel("Count")
plt.xticks(np.arange(0, len(intervals) * width, width), labels=np.arange(0, len(intervals) * 5, 5))
plt.yticks(np.arange(0, 11, 1))
plt.xlim(0, (len(intervals) - 1) * width)
plt.ylim(0, 10)

plt.show()
