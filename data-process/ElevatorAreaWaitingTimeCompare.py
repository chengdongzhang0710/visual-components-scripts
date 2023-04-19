import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as psl


# set global style
psl.use("seaborn-talk")


# plot figure
labels = ["Factory #1 Up", "Factory #1 Left", "Factory #1 Right"]

plt.figure(figsize=(12, 9))

plt.grid(axis="y")

x1 = np.array([0, 6, 12])
x2 = np.array([2, 8, 14])
x = np.array([1, 7, 13])

y1 = [19.5, 1.6, 1.2]
y2 = [19.5, 1.6, 6.4]

plt.bar(x1, y1, width=1, label="Before")
plt.bar(x2, y2, width=1, label="After")

plt.title("Elevator Area Average Waiting Time Compare")
plt.xlabel("Factory Area")
plt.ylabel("Waiting Time")
plt.xticks(x, labels=labels)
plt.yticks((np.arange(0, 31, 5)))
plt.ylim(0, 30)

plt.legend(loc="upper right")

plt.show()
