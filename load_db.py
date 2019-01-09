from sqlalchemy import create_engine
import pandas as pd
import os
from decimal import *


csv_data = pd.read_csv(
    './assets/IHME-GBD_2017_DATA-37d305ef-1.csv',
    error_bad_lines=False
)
df = pd.DataFrame(csv_data)

# Adjust NaN values in each column, and generally clean data set
# df['id'] = df['id'].fillna(0)
del df['measure_id']
del df['measure_name']
df['location_id'] = df['location_id'].fillna(0)
df['location_name'] = df['location_name'].fillna('unknown')
df['sex_id'] = df['sex_id'].fillna(0)
df['sex_name'] = df['sex_name'].fillna('unknown')
del df['age_id']
del df['age_name']
del df['cause_id']
del df['cause_name']
del df['metric_id']
del df['metric_name']
df['year'] = df['year'].fillna(0)
df['val'] = df['val'].fillna(0)
df['upper'] = df['upper'].fillna(0)
df['lower'] = df['lower'].fillna(0)
df['sex_percentage'] = float(1.0)
df['rank'] = 0
df['percent_change'] = float(0.0)
df['average_percent_change'] = float(0.0)
df['raw_decrease_from_peak'] = float(0.0)
df['raw_increase_from_min'] = float(0.0)
df['avg_percent_change_since_peak'] = float(0.0)
df['avg_percent_change_since_min'] = float(0.0)
df['peak'] = float(0.0)
df['min'] = float(0.0)

# Let's find the val rank for each year/sex per country.
for year in df['year'].unique():
    for sex in df['sex_id'].unique():
        df_current = df[(df['sex_id']==sex) & (df['year']==year)].sort_values(by=['val'], ascending=False).reset_index()
        for index, row in df_current.iterrows():
            df.at[row['index'], 'rank'] = index + 1

# Calculate %change each year as well as data for calculating the sharpest increases/declines
for country in df['location_name'].unique():
    for sex in df['sex_id'].unique():
        df_country = df[(df['sex_id']==sex) & (df['location_name']==country)].sort_values(by=['year'])
        previous_val = df_country[(df_country['year']==1990)]['val']
        year_of_peak =  df_country.loc[df_country['val'].idxmax()]['year']
        year_of_min =  df_country.loc[df_country['val'].idxmin()]['year']
        total_change = 0
        total_change_since_peak = 0
        total_change_since_min = 0
        years_since_peak = 0
        years_since_min = 0
        for index, row in df_country[1:].iterrows():
            percent_change = (row['val'] - previous_val)/previous_val
            total_change += percent_change
            if(row['year'] > year_of_peak):
                total_change_since_peak += percent_change
                years_since_peak+=1
            if(row['year'] > year_of_min):
                total_change_since_min += percent_change
                years_since_min+=1
            previous_val = row['val']
            df.at[index, 'percent_change'] = percent_change
        df.at[index, 'average_percent_change'] = total_change/26
        try:
            df.at[index, 'avg_percent_change_since_peak'] = total_change_since_peak/(years_since_peak)
        except ZeroDivisionError:
            pass
        try:
            df.at[index, 'avg_percent_change_since_min'] = total_change_since_min/(years_since_min)
        except ZeroDivisionError:
            pass

        df.at[index, 'peak'] = Decimal(df_country['val'].max())
        df.at[index, 'min'] = Decimal(df_country['val'].min())
        df.at[index, 'raw_decrease_from_peak'] = float(df_country[(df['year']==2017)]['val']) - df_country['val'].max()
        df.at[index, 'raw_increase_from_min'] = float(df_country[(df['year']==2017)]['val']) - df_country['val'].min()

# The following block appends world data (annual means) to the dataset
df_world = pd.DataFrame(columns=['id', 'location_id', 'location_name', 'sex_id', 'sex_name', 'year', 'val', 'upper', 'lower', 'sex_percentage', 'rank', 'percent_change', 'average_percent_change', 'raw_decrease_from_peak', 'raw_increase_from_min', 'avg_percent_change_since_peak', 'avg_percent_change_since_min', 'peak', 'min'])

index = df.count()['location_id']

for year in df['year'].unique():
    for sex in df['sex_id'].unique():
        df_world.at[index, 'id'] = None
        df_world.at[index, 'location_id'] = int(0)
        df_world.at[index, 'location_name'] = 'World'
        df_world.at[index, 'sex_id'] = int(sex)
        df_world.at[index, 'sex_name'] = 'Male' if sex == 1 else 'Female' if sex == 2 else 'Both'
        df_world.at[index, 'year'] = int(year)
        df_world.at[index, 'val'] = df[(df['sex_id'] == sex) & (df['year'] == year)]['val'].mean()
        df_world.at[index, 'upper'] = df[(df['sex_id'] == sex) & (df['year'] == year)]['upper'].mean()
        df_world.at[index, 'lower'] = df[(df['sex_id'] == sex) & (df['year'] == year)]['lower'].mean()
        df_world.at[index, 'rank'] = int(0)
        df_world.at[index, 'sex_percentage'] = 1.0
        df_world.at[index, 'percent_change'] = 0.0
        df_world.at[index, 'average_percent_change'] = 0.0
        df_world.at[index, 'raw_decrease_from_peak'] = 0.0
        df_world.at[index, 'raw_increase_from_min'] = 0.0
        df_world.at[index, 'avg_percent_change_since_peak'] = 0.0
        df_world.at[index, 'avg_percent_change_since_min'] = 0.0
        df_world.at[index, 'peak'] = 0.0
        df_world.at[index, 'min'] = 0.0
        # df_world.at[index, 'id'] = index

        index += 1

df_world = df_world.sort_values(by=['year'])
for sex in df_world['sex_id'].unique():
    df_sex = df_world[(df_world['sex_id']==sex)].sort_values(by=['year'])
    previous_val = df_sex[(df_sex['year']==1990)]['val']
    total_percent_change = 0
    for index, row in df_sex[1:].iterrows():
        percent_change = float((row['val'] - previous_val)/previous_val)
        total_percent_change += percent_change
        previous_val = row['val']
        df_world.at[index, 'percent_change'] = percent_change
    df_world.at[index, 'average_percent_change'] = float(total_percent_change/26)

df = df.append(df_world, sort=True)

# For each country determine what % of deaths are male/female
# It's not the cleanest, but I'm storing the female value with the "both" rows for ease of access.

for country in df['location_name'].unique():
    for year in df['year'].unique():
        df_current = df[(df['location_name']==country) & (df['year']==year)].sort_values(by=['sex_id'])
        male_rate = float(df_current[(df['sex_id']==1)]['val'])
        female_rate = float(df_current[(df['sex_id']==2)]['val'])
        both_rate = float(df_current[(df['sex_id']==3)]['val'])
        female_percentage = (female_rate*(both_rate-male_rate))/(both_rate*(female_rate-male_rate))
        male_percentage = 1 - female_percentage
        df.at[df_current.index[0], 'sex_percentage'] = male_percentage
        df.at[df_current.index[0]+1, 'sex_percentage'] = female_percentage
        df.at[df_current.index[0]+2, 'sex_percentage'] = female_percentage

db_protocol = 'postgresql'
db_host = os.environ.get('DB_HOST', '')
db_user = os.environ.get('DB_USER', '')
db_password = os.environ.get('DB_PASSWORD', '')
db_name = os.environ.get('DB_NAME', '')

engine = create_engine('{}://{}:{}@{}:5432/{}'.format(
    db_protocol, db_user, db_password, db_host, db_name
))

df.to_sql('opioid_api_opioids', engine, if_exists='replace')
