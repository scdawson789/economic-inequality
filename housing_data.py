import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math

sns.set()

citation_text = """U.S. Census Bureau, Median Family Income in the US - https://fred.stlouisfed.org/series/MEFAINUSA646N, February 15, 2025.
U.S. CB and HUD, Median Sales Price of Houses Sold for the United States - https://fred.stlouisfed.org/series/MSPUS, February 15, 2025."
Freddie Mac, 30-Year Fixed Rate Mortgage Avg in US - https://fred.stlouisfed.org/series/MORTGAGE30US, February 15, 2025."""

pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)

# Read in mortgage interest rate
interest = pd.read_csv("data\\mortgage_30_year_fixed.csv", index_col=[0])
interest.index = pd.to_datetime(interest.index)
interest = interest.resample('YE-DEC').agg('mean')
interest = interest.rename(columns={'MORTGAGE30US': 'mortgage_rate'})
interest.index = interest.index.year

# median housing data
median_houses = pd.read_csv("data\\median_sale_price_us_houses.csv", index_col=[0])
median_houses.index = pd.to_datetime(median_houses.index)
median_houses = median_houses.resample('YE-DEC').agg('mean')
median_houses = median_houses.rename(columns={'MSPUS': 'median_home_price'})
median_houses.index = median_houses.index.year

# Median family income
median_family = pd.read_csv("data\\median_family_income_fred.csv", index_col=[0], header=0)
median_family.index = pd.to_datetime(median_family.index)
median_family = median_family.rename(columns={'MEFAINUSA646N': "median_family_income"})
median_family.index = median_family.index.year

final_df = pd.concat([median_family, median_houses], axis=1)
final_df = final_df.dropna(axis=0, how='any')
final_df['med_home_to_med_income'] = final_df['median_home_price']/ final_df['median_family_income']

full_df = final_df.copy()
full_df = pd.concat([interest, full_df], axis=1)
full_df = full_df.dropna(axis=0, how='any')

# Get the monthly mortgage rate
full_df['mortgage_rate'] = full_df['mortgage_rate']/100/12

top_func = lambda x: x*(1 + x)**360
bottom_func = lambda x: (1 + x)**360 - 1
full_df['top_funct'] = full_df['mortgage_rate'].map(top_func)
full_df['bottom_funct'] = full_df['mortgage_rate'].map(bottom_func)
full_df['median_home_pymnt'] = (full_df['median_home_price'] * full_df['top_funct']) / full_df['bottom_funct']

full_df = full_df.drop(['top_funct', 'bottom_funct'], axis=1)

#multiple monthly payment to get annual payment and divide by median family income
full_df['pymt_pct_income'] = full_df['median_home_pymnt']*12/ full_df['median_family_income']

print(final_df)

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,8))
plt.suptitle("Median Sale Price of US Home to Median Family Income")
ax.set_xlabel("Year")
ax.set_ylabel("Median Sale Price")
ax.plot(final_df.index, final_df.med_home_to_med_income, color='blue', label='Median Home price to Median Family Income')

plt.figtext( .5, .1, citation_text, ha='center', fontsize=10, style='italic')

fig.tight_layout(rect=[0,.15,1,1])
plt.legend(loc='best')
plt.show()
print(full_df)

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,8))
plt.suptitle("30-year Mortgage payments as Pct of Income", fontsize=17)
ax.set_xlabel("Year")
ax.set_ylabel("Mortgage payments as pct of income")
ax.plot(full_df.index, full_df.pymt_pct_income, color='blue', label='Median home payment (med price + interest) as pct of income')

plt.figtext( .5, .1, citation_text, ha='center', fontsize=10, style='italic')

fig.tight_layout(rect=[0,.15,1,1])

plt.legend(loc='best')
plt.show()

