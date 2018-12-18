from sqlalchemy import create_engine
import pandas as pd
import os


csv_data = pd.read_csv(
    './assets/IHME-GBD_2017_DATA-37d305ef-1.csv',
    error_bad_lines=False
)
df = pd.DataFrame(csv_data)

# Adjust NaN values in each column, and generally clean data set
# df['ID'] = df['ID'].fillna(0)
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
df['rank'] = 0

# Let's find the val rank for each year/sex per country.
for year in df['year'].unique():
    for sex in df['sex_id'].unique():
        df_current = df[(df['sex_id']==sex) & (df['year']==year)].sort_values(by=['val'], ascending=False).reset_index()
        for index, row in df_current.iterrows():
            df.at[row['index'], 'rank'] = index + 1

# The following block appends world data (annual means) to the dataset
df_world = pd.DataFrame(columns=['id', 'location_id', 'location_name', 'sex_id' 'sex_name', 'year', 'val', 'upper', 'lower'])

index = df.count()['location_id'] + 1

for year in df['year'].unique():
    for sex in df['sex_id'].unique():
        df_world.at[index, 'location_id'] = int(0)
        df_world.at[index, 'location_name'] = 'World'
        df_world.at[index, 'sex_id'] = int(sex)
        df_world.at[index, 'sex_name'] = 'Male' if sex == 1 else 'Female' if sex == 2 else 'Both'
        df_world.at[index, 'year'] = int(year)
        df_world.at[index, 'val'] = df[(df['sex_id'] == sex) & (df['year'] == year)]['val'].mean()
        df_world.at[index, 'upper'] = df[(df['sex_id'] == sex) & (df['year'] == year)]['upper'].mean()
        df_world.at[index, 'lower'] = df[(df['sex_id'] == sex) & (df['year'] == year)]['lower'].mean()
        index += 1

# import pdb; pdb.set_trace()

df = df.append(df_world, sort=True)



db_protocol = 'postgresql'
db_host = os.environ.get('DB_HOST', '')
db_user = os.environ.get('DB_USER', '')
db_password = os.environ.get('DB_PASSWORD', '')
db_name = os.environ.get('DB_NAME', '')



engine = create_engine('{}://{}:{}@{}:5432/{}'.format(
    db_protocol, db_user, db_password, db_host, db_name
))



df.to_sql('opioid_api_opioids', engine, if_exists='replace', index=False)
