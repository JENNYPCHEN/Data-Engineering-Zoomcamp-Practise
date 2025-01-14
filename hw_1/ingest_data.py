import os
import argparse
import gzip
import shutil
from time import time
import pandas as pd
from sqlalchemy import create_engine

def main(params):
    user = os.getenv('USER')
    password = os.getenv('PASSWORD')
    host = os.getenv('HOST')
    port = os.getenv('PORT')
    db = os.getenv('DB')
    table_name = os.getenv('TABLE_NAME')
    url = os.getenv('URL')
    zones_url = os.getenv('ZONES_URL')
    csv_name = 'output.csv'
    gz_name = 'output.csv.gz'
    zones_csv_name = 'taxi_zone_lookup.csv'

    # download the CSV files
    os.system(f"wget {url} -O {gz_name}")
    os.system(f"wget {zones_url} -O {zones_csv_name}")

    # decompress the file
    with gzip.open(gz_name, 'rb') as f_in:
        with open(csv_name, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    df_zones = pd.read_csv(zones_csv_name)

    df = next(df_iter)

    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    df_zones.to_sql(name='taxi_zones', con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')

    while True:
        try:
            t_start = time()

            df = next(df_iter)

            df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
            df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

            df.to_sql(name=table_name, con=engine, if_exists='append')

            t_end = time()

            print('inserted another chunk, took %.3f second' % (t_end - t_start))
        except StopIteration:
            print('completed')
            break

if __name__ == '__main__':
    main(None)