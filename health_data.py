import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()

# Read in data
data = pd.read_csv("data\\EPI Data Library - Health insurance coverage.csv", header=0, index_col=[0])

# remove percentage signs and convert to float
clean_funct = lambda x: float(x.replace("%", ""))
data = data.map(clean_funct)


# prep labels and colors
cols = data.columns = ['All', 'bottom_fifth', 'second_fifth', 'middle_fifth', 'fourth_fifth', 'top_fifth']
colors = ['blue', 'purple', 'green', 'orange', 'red', 'magenta']

fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 8))
fig.suptitle("Health Insurance")
for i in range(len(data.columns)):
    ax.plot(data.index, data[cols[i]], color=colors[i], label=cols[i])
ax.set_xlabel("Year")
ax.set_ylabel("Percent")

plt.legend(loc='best')
plt.show()

print(data)