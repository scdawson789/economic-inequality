import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)
sns.set()

citation_text = ("""Macrotrends: https://www.macrotrends.net/1365/jobless-claims-historical-chart
                 Economic Policy Institute, State of Working America Data Library, [Employment-to-population-ratio], 2024""")

race_data = pd.read_csv("data\\EPI Data Library_Underemployment_race.csv", index_col=[0], header=0)

general_data = pd.read_csv("data\\EPI Data Library_Underemployment_race.csv", index_col=[0], header=0)
t_function = lambda x: float(str(x).replace("%", ""))
general_data = general_data.map(t_function)
general_data.index = pd.to_datetime(general_data.index)

#drop NA Values
general_data = general_data.dropna(axis=0, how='any')
general_data['year'] = general_data.index.year
long_form = pd.melt(general_data, id_vars='year', value_vars=['All', 'Black', 'Hispanic', 'White'])
long_form.columns = ['year', 'race', 'underemployment_pct']

long_form = long_form.groupby(['year', 'race']).agg('mean').reset_index()
long_form = pd.DataFrame(long_form)
print(long_form)

sns.lineplot(x='year', y='underemployment_pct', hue='race', data=long_form)

plt.title("Underemployment by race")
plt.xlabel("Year")
plt.ylabel("Underemployment Percent")
plt.show()

emp_to_pop = pd.read_csv("data\\EPI Data Library - Employment-to-population ratio.csv", index_col=[0], header=0)

emp_to_pop = emp_to_pop.map(t_function)
emp_to_pop.index = pd.to_datetime(emp_to_pop.index)
emp_to_pop['years'] = emp_to_pop.index.year

emp_to_pop = emp_to_pop.reset_index()
emp_to_pop.columns = ['Date', 'All', 'Women', 'Men', 'Black', 'Hispanic', 'White', 'Black_Women', 'Black_Men', 'Hispanic_Women',
                                                              'Hispanic_Men', 'White_Women', 'White_Men', 'years']
long_emp_to_pop = pd.melt(emp_to_pop, id_vars=['Date', 'years'], value_vars=['Black_Women', 'Black_Men', 'Hispanic_Women',
                                                              'Hispanic_Men', 'White_Women', 'White_Men'])
long_emp_to_pop.columns = ['Date', 'years', 'race_gender', 'pct_employed']
long_emp_to_pop = long_emp_to_pop.drop('Date', axis=1)
long_emp_to_pop = long_emp_to_pop.groupby(['years', 'race_gender']).agg('mean').reset_index()
long_emp_to_pop = pd.DataFrame(long_emp_to_pop)


sns.lineplot( x='years', y='pct_employed', hue='race_gender', data=long_emp_to_pop)

plt.title("Percent Employed by Race and Gender")
plt.xlabel("Year")
plt.ylabel("Employment Percent")
plt.tight_layout(rect=[0,0,.8,1])
plt.legend(bbox_to_anchor=(1,1), loc='upper left', fontsize=8)
plt.show()


citation_text2 = "https://fred.stlouisfed.org/series/CIVPART/"
labor_participation = pd.read_csv("data\\Labor_force_participation_rate.csv", index_col=0)
labor_participation.index = pd.to_datetime(labor_participation.index)
labor_participation_annual = labor_participation.resample('YE-DEC').mean()
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,8))
plt.title("Percent Participating in Labor Force")
plt.xlabel("Year")
plt.ylabel("Percent Participation")
plt.tight_layout(rect=[0,0,1,1])
ax.set_ylim([50,70])
ax.plot(labor_participation_annual.index, labor_participation_annual.CIVPART, label='civic participation')
plt.annotate(text="https://fred.stlouisfed.org/series/CIVPART/", xy=(), xytext=())
plt.show()
print(labor_participation_annual)




jobless = pd.read_csv("data\\jobless-claims-historical-chart.csv", skiprows=list(range(15)), header=[0])
print(jobless)