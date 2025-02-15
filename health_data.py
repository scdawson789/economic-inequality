import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#sns.set()

# Read in data
data = pd.read_csv("data\\EPI Data Library - Health insurance coverage.csv", header=0, index_col=[0])
citation_text = "Source: Economic Policy Institute, State of Working America Data Library, “[Health insurance coverage],” 2024."

# remove percentage signs and convert to float
clean_funct = lambda x: float(x.replace("%", ""))
data = data.map(clean_funct)


# prep labels and colors
cols = data.columns = ['All', 'bottom_fifth', 'second_fifth', 'middle_fifth', 'fourth_fifth', 'top_fifth']
colors = ['blue', 'purple', 'green', 'orange', 'red', 'magenta']

fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 8))
fig.suptitle("Health Insurance", fontsize=20)
for i in range(len(data.columns)):
    ax.plot(data.index, data[cols[i]], color=colors[i], label=cols[i])
ax.set_title("Company provided healthcare", fontsize=16)
ax.set_xlabel("Year", fontsize=14)
ax.set_ylabel("Percent of Workers", fontsize=14)
ax.set_xlim([1976, 2020])
ax.spines[['right', 'top']].set_visible(False)
plt.grid(False)

for i in range(len(data.columns)):
    plt.annotate(data.iloc[0,i], xy=(2019,data.iloc[0,i]))
    plt.annotate(data.iloc[40,i], xy=(1977, data.iloc[40,i]))

plt.figtext(.5, .05, citation_text, ha='center')
fig.tight_layout(rect=[0,.1, 1, 1])
plt.legend(loc=(.85, .85))
plt.show()

print(data)