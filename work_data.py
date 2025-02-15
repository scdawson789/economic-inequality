import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)
sns.set()

citation_text = "Macrotrends: https://www.macrotrends.net/1365/jobless-claims-historical-chart"

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



emp_to_pop = pd.read_csv("data\\EPI Data Library - Employment-to-population ratio.csv")

labor_participation = pd.read_csv("data\\Labor_force_participation_rate.csv")

jobless = pd.read_csv("data\\jobless-claims-historical-chart.csv", skiprows=list(range(15)), header=[0])