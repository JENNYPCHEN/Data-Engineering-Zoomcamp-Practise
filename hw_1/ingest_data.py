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

    # load the data into a pandas dataframe
    df = pd.read_csv(csv_name)
    print(f"Dataframe loaded with {len(df)} records")

    # create a database connection
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    print("Database connection established")

    # load data into the database
    df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
    print(f"Data loaded into table {table_name}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')
    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table where we will write the results to')
    parser.add_argument('--url', help='url of the csv file')
    parser.add_argument('--zones_url', help='url of the zones csv file')

    args = parser.parse_args()

    main(args)