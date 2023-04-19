import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as psl
import datetime


# set global style
psl.use("seaborn-talk")


# data collect
df = pd.read_csv("ElevatorAreaBufferCount.csv")
df.drop("Simulation Time", axis=1, inplace=True)
labels = ["Factory #1 Up", "Factory #1 Right", "Factory #1 Left", "Factory #3", "Factory #9 Right",
          "Factory #9 Left", "Factory #9 Down"]
df.columns = labels.copy()

# plot figure
x = []
start = datetime.datetime(2022, 3, 1, 8, 0)
for i in range(len(df[labels[0]])):
    now = start + datetime.timedelta(minutes=i)
    x.append(now.strftime("%H:%M"))

plt.figure(figsize=(18, 9))

plt.grid(axis="y")

for label in labels:
    plt.plot(x, np.array(df[label]), label=label)

plt.title("Elevator Area Buffer Count")
plt.xlabel("Time")
plt.ylabel("Number Count")
plt.xticks(np.arange(0, len(x), 60))
plt.yticks(np.arange(0, 16, 1))
plt.ylim(0, 15)

plt.legend(loc="upper left")

plt.show()
