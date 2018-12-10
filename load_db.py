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

# df = df.sort_values(by=['usd_pledged'], ascending=False)

db_protocol = 'postgresql'
db_host = os.environ.get('DB_HOST', '')
db_user = os.environ.get('DB_USER', '')
db_password = os.environ.get('DB_PASSWORD', '')
db_name = os.environ.get('DB_NAME', '')

print('Prior to create engine')
# print(df)

engine = create_engine('{}://{}:{}@{}:5432/{}'.format(
    db_protocol, db_user, db_password, db_host, db_name
))

print('Prior to df.to_sql command')
print('{}://{}:{}@{}:5432/{}'.format(
    db_protocol, db_user, db_password, db_host, db_name
))

df.to_sql('opioid_api_opioids', engine, if_exists='append', index=False)
