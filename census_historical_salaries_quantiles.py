import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl

sns.set()


def calculate_cost_living(start, multiple, length):
    values = [start]
    for i in range(1, length):
        values.append(round(values[-1] * multiple,3))
    print(values)
    return values


def get_percentile_change(df):
    temp = df.columns
    temp_df = df.copy()
    new_col_name1 = 'ratio_'+ str(temp[0])+"_" + str(temp[1])
    temp_df[new_col_name1] = df[temp[1]]/df[temp[0]]
    temp_df = temp_df.sort_index()

    print(temp_df)
    return temp_df


pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)

rows_to_skip = list(range(0,5)) + list(range(65,90,1))

data = pd.read_csv("data\\Census_historcal_salaries_quantiles.csv", index_col=[0], skiprows=rows_to_skip,header=[0])

citation_text= """Source: U.S. Census Bureau, Current Population Survey, 1968 to 2024 Annual Social and Economic Supplements (CPS ASEC).
Note from US CB: Median income estimates are currently calculated using linear interpolation and $2,500 intervals. 
Between 1976 and 1987, some median income estimates were also calculated using Pareto interpolation."""

# replace erroneous characters
rows = [ int(row.split()[0]) for row in data.index]
data.index = rows

# remove space in column header with underscore
cols = data.columns.str.replace(" ", "_").str.replace("\n", "")
cols = cols.str.replace("/", "_div_")
data.columns = cols

# replace commas in the numbers and cast as numeric
func_int = lambda x: int(str(x).replace(",", ""))
data.iloc[:,:10] = data.iloc[:,:10].map(func_int)

data = data.reset_index().rename(columns={'index': 'year'})
data = data.drop_duplicates(subset=['year'], keep='first')
data = data.set_index('year')

agg_data = data[['10th_percentile', '20th_percentile', '30th_percentile', '40th_percentile',
      '50th_percentile(median)', '60th_percentile', '70th_percentile',
      '80th_percentile', '90th_percentile', '95th_percentile']].copy()
col_vals = agg_data.columns
col_names = [col.split("_")[0] for col in col_vals]

agg_data = agg_data.sort_index()


for col in range(len(agg_data.columns)-1):

    bin_yrs = [1966, 1970, 1980, 1990, 2000, 2010, 2020, 2024]
    bin_labels = ['1967 - 1969', '1970 - 1979', '1980 - 1989', '1990 - 1999', '2000 - 2009', '2010 - 2019', '2020 - 2023']


    temp_df = get_percentile_change(agg_data.iloc[:,col: col+2])
    list_cols = [col for col in temp_df.columns]
    col_name = list_cols[2]


    temp_df['binned'] = pd.cut(temp_df.index, bins=bin_yrs, labels=bin_labels, right=False )

    result = temp_df.groupby('binned', as_index=False, observed=False)[col_name].agg(['mean', 'max', 'min', 'std'])

    result.columns = ['years', 'mean_val', 'max_val', 'min_val', 'std_dev']
    result.iloc[:, 1:] = result.iloc[:, 1:].map(lambda x: round(x,6))

    labels = ['20th_div_10th', '30th_div_20th', '40th_div_30th', '50th_div_40th', '60th_div_50th', '70th_div_60th', '80th_div_70th', '90th_div_80th', '95th_div_90th']
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(14, 8))
    fig.tight_layout(pad=3.0)

    x, y = labels[col].split("_div_")
    plt.suptitle("Ratio between " + x + " and " + y + " Percentiles")
    ax.set_title("Decade Data: Max, Min, Mean")
    ax.set_xlabel("Year")
    ax.set_xticks(range(len(result.min_val)))
    ax.set_xticklabels(bin_labels, fontsize=16)
    ax.set_ylabel("Ratio between: " + x + " and " + y + " pct")
    ax.plot(result.years, result.mean_val, label=labels[col], color='slategray')
    ax.fill_between(x=result.years.to_list(), y1=result.min_val.to_list(), y2=result.max_val.to_list(),color=mpl.colors.to_rgba('brown', 0.15) )


    plt.show()

label_data = agg_data.loc[[1967, 2023]]

change_df = label_data.transpose().astype('int')

change_df.columns = ['1967', '2023']

change_df = change_df.assign(pct_chg = round((change_df['2023'] - change_df['1967'])/ change_df['1967'] *100, 2))

change_df.columns = ['1967', '2023', 'pct_chg']

fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(12,8))

ax.set_title("Income by Quantile", fontsize=20)
ax.set_xlabel(" Year")
ax.set_ylabel("Income in by Quantile")
ax.set_ylim([0,350000])
colors = ['red', 'lightsalmon', 'darkorange', 'yellow', 'gold', 'lime', 'forestgreen', 'lightsteelblue', 'blue', 'darkorchid']

for col in range(len(agg_data.columns)):
    ax.plot(agg_data.index, agg_data[agg_data.columns[col]], color=colors[col], label=agg_data.columns[col])

ax.spines[['right', 'top']].set_visible(False)

plt.annotate(text="Percent increase", xy=(2017, 340000), xytext=(2017, 340000))
for i in range(len(change_df)):
    plt.annotate(change_df.iloc[i,2], (2023, change_df.iloc[i,1]))

plt.figtext(.5, .05, citation_text, ha='center')
fig.tight_layout(rect=[0, .1, 1, 1])
ax.legend(loc='best')
plt.show()