# %%
import pandas as pd
import seaborn as sns

df = pd.read_csv('crime-housing-austin-2015.csv')
df.head()
df.columns

# %%
seen = []
for index, row in df.iterrows():
    value = row['Highest_NIBRS_UCR_Offense_Description']
    if value not in seen:
        seen.append(value)
print(seen)


# %%
# Graph crimes with x and y coordinates (which are close to transportation?)
# Compare amount of crimes in zip codes with income/race
# %%
from scipy.stats import ttest_ind

crime = 'Highest_NIBRS_UCR_Offense_Description'
df[df.Highest_NIBRS_UCR_Offense_Description == 'Agg Assault']
agg = df[df.Highest_NIBRS_UCR_Offense_Description == 'Agg Assault']
# %%
sns.scatterplot(x=agg.X_Coordinate, y=agg.Y_Coordinate)
# %%

agg['Medianhouseholdincome'] = agg['Medianhouseholdincome'].str.replace('$', '').astype('float')
zip_codes = agg.groupby(by=['Zip_Code_Crime']).agg({'Medianhouseholdincome': 'mean', 'Key': 'count'}).reset_index().dropna()
sns.scatterplot(x=zip_codes['Medianhouseholdincome'], y=zip_codes['Key'])
# %%
# Standardizing median household income vs amount of crimes
from scipy.stats import ttest_ind
from sklearn import preprocessing

names = zip_codes.columns
scaler = preprocessing.StandardScaler()

scaled_df = scaler.fit_transform(zip_codes)
scaled_df = pd.DataFrame(scaled_df, columns=names)

sns.distplot(scaled_df['Medianhouseholdincome'], label='Median Household Income', hist = False)

#%% 
sns.distplot(scaled_df['Medianhouseholdincome'], label='Median Household Income', hist=False)
sns.distplot(scaled_df['Key'], label='Number of aggravated assaults', hist=False)
ttest_ind(scaled_df['Medianhouseholdincome'], scaled_df['Key'])

scaled_df.corr(method='pearson')
zip_codes.corr(method='pearson')

#%%
from sklearn import preprocessing

sns.distplot(agg['Medianhouseholdincome'], norm_hist=True, hist = False)
scaler = preprocessing.StandardScaler()

scaled_df = scaler.fit_transform(agg)
scaled_df = pd.DataFrame(scaled_df, columns='Medianhouseholdincome')

sns.scatterplot(scaled_df)
# %%
import datetime
import time
from scipy.stats import ttest_ind

point = 50000
poor = agg[agg['Medianhouseholdincome'] <= point]
rich = agg[agg['Medianhouseholdincome'] > point]
for index, row in poor.iterrows():
    value = float(time.mktime(datetime.datetime.strptime(row['Report_Date'], '%d-%b-%y').timetuple()))
    poor.at[index, 'Report_Date'] = value
for index, row in rich.iterrows():
    value = float(time.mktime(datetime.datetime.strptime(row['Report_Date'], '%d-%b-%y').timetuple()))
    rich.at[index, 'Report_Date'] = value
sns.distplot(poor['Report_Date'], label=f'Less than ${point}', hist=False)
sns.distplot(rich['Report_Date'], label=f'More than ${point}', hist=False)
ttest_ind(poor['Report_Date'], rich['Report_Date'])

# %%
