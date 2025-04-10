import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
plt.rcParams["figure.figsize"] = (16,8)
sns.set()

def calculate_difference(start, values):
    vals = [start]
    values = list(values)
    for i in range(1, len(values)):
        temp = values[i] - values[i-1]
        vals.append(temp)
    return vals


# Read in data
data = pd.read_csv("data\\EPI Data Library - Health insurance coverage.csv", header=0, index_col=[0])
health_premiums = pd.read_csv("data\\health_premiums.csv", header=0, skiprows=[0], index_col='Year')
health_premiums['change'] = health_premiums.shift(-1)/health_premiums - 1
health_premiums['change_pct'] = round(health_premiums.change.shift(1).fillna(0) * 100 , 1)
health_premiums['monthly_cost'] = health_premiums['Cost']/12
health_premiums['diff'] = calculate_difference(health_premiums['Cost'].iloc[0], health_premiums.Cost.values)
health_premiums['change_pct_text'] = health_premiums['change_pct'].astype(str) + "%"
health_premiums['cost_shift'] = health_premiums['diff'].cumsum().shift(1).fillna(0)

health_premiums.drop('change', axis=1, inplace=True)

# Median family income
median_family = pd.read_csv("data\\median_family_income_fred.csv", index_col=[0], header=0)
median_family.index = pd.to_datetime(median_family.index)
median_family = median_family.rename(columns={'MEFAINUSA646N': "median_family_income"})
median_family.index = median_family.index.year

#health_premiums = health_premiums.join(median_family, how='inner')

median_personal = pd.read_csv("data\\median_personal_income_US_fred.csv", index_col=[0], header=0)
median_personal.index = pd.to_datetime(median_personal.index)
median_personal = median_personal.rename(columns={'MEPAINUSA646N': 'median_personal_income'})
health_premiums2 = health_premiums.join(median_personal, how='inner')



citation_text = "Source: Economic Policy Institute, State of Working America Data Library, “[Health insurance coverage],” 2024."
citation_text3 = "U.S. Census Bureau, Median Family Income in the US - https://fred.stlouisfed.org/series/MEFAINUSA646N, February 15, 2025."

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

lower = health_premiums[['Cost', 'cost_shift']].min(axis=1)
upper = health_premiums[['Cost', 'cost_shift']].max(axis=1)
mid = (lower + upper)/2
print(mid)



