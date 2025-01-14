"""
Question 1. Understanding docker first run
Run docker with the python:3.12.8 image in an interactive mode, use the entrypoint bash.

First, create a Dockerfile with the following content:

FROM python:3.12.8

ENTRYPOINT ['bash']

Second, build the image with the following command: (Don't forget to replace the image name with your own)

docker build -t my_python_image .

Third, run the image with the following command:

docker run -it my_python_image

Fourth, check the pip version with the following command:

pip -V

What is the pip version?
pip 24.3.1 from /usr/local/python/3.12.1/lib/python3.12/site-packages/pip (python 3.12)
"""

"""
Question 2. Understanding Docker networking and docker-compose
Given the following docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?

services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin  

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data

the answer is postgres:5433, hostname is postgres and port is 5433.
"""
"""
Prepare Postgres:

First set up the Dockerfile:
FROM python:3.9.1

# Install wget to download the CSV file and other necessary packages
RUN apt-get update && apt-get install -y wget && \
    pip install pandas sqlalchemy psycopg2-binary pgcli

WORKDIR /app
COPY ingest_data.py ingest_data.py 

ENTRYPOINT [ "python", "ingest_data.py" ]

Second, create the ingest_data.py file

Third, create the docker-compose.yaml file

Fourth, build the image

Fifth, run the image

Sixth, run Docker Compose

Seventh, register the server in pgAdmin
To solve the pdadmin sessions permission issue, I use the following command to resolve it:
mkdir -p ./data_pgadmin/sessions
sudo chown -R 5050:5050 ./data_pgadmin
"""
"""
Question 3. Trip Segmentation Count
During the period of October 1st 2019 (inclusive) and November 1st 2019 (exclusive), how many trips, respectively, happened:

Up to 1 mile
In between 1 (exclusive) and 3 miles (inclusive),
In between 3 (exclusive) and 7 miles (inclusive),
In between 7 (exclusive) and 10 miles (inclusive),
Over 10 miles

SELECT
    SUM(CASE WHEN trip_distance <= 1 THEN 1 ELSE 0 END) AS "Up to 1 mile",
    SUM(CASE WHEN trip_distance > 1 AND trip_distance <= 3 THEN 1 ELSE 0 END) AS "1 to 3 miles",
    SUM(CASE WHEN trip_distance > 3 AND trip_distance <= 7 THEN 1 ELSE 0 END) AS "3 to 7 miles",
    SUM(CASE WHEN trip_distance > 7 AND trip_distance <= 10 THEN 1 ELSE 0 END) AS "7 to 10 miles",
    SUM(CASE WHEN trip_distance > 10 THEN 1 ELSE 0 END) AS "Over 10 miles"
FROM green_taxi_trips
WHERE lpep_pickup_datetime >= '2019-10-01' AND lpep_pickup_datetime < '2019-11-01';

The answer is 100027	184314	82575	17019	16033
"""
"""
Question 4. Longest trip for each day
Which was the pick up day with the longest trip distance? Use the pick up time for your calculations.

Tip: For every day, we only care about one single trip with the longest distance.

2019-10-11
2019-10-24
2019-10-26
2019-10-31

SELECT
    DATE(lpep_pickup_datetime) AS pickup_date,
    MAX(trip_distance) AS longest_trip_distance
FROM green_taxi_trips
WHERE DATE(lpep_pickup_datetime) IN ('2019-10-11', '2019-10-24', '2019-10-26', '2019-10-31')
GROUP BY pickup_date
ORDER BY pickup_date;

The answer is "2019-10-31"	515.89
"""
"""
Question 5. Three biggest pickup zones
Which were the top pickup locations with over 13,000 in total_amount (across all trips) for 2019-10-18?

Consider only lpep_pickup_datetime when filtering by date.

East Harlem North, East Harlem South, Morningside Heights
East Harlem North, Morningside Heights
Morningside Heights, Astoria Park, East Harlem South
Bedford, East Harlem North, Astoria Park

SELECT SUM(trip_distance), taxi_zones."Zone"
FROM green_taxi_trips
join taxi_zones on taxi_zones."LocationID" =green_taxi_trips."PULocationID"
WHERE DATE(lpep_pickup_datetime) = '2019-10-18'
GROUP BY taxi_zones."Zone"
--Having SUM(trip_distance) >13000
Order by sum(trip_distance) desc
limit 3;

None is over >13000, so the answer is None. If no such condition, the answer is East Harlem North, East Harlem South, Elmhurst

"""
"""
Question 6. Largest tip
For the passengers picked up in Ocrober 2019 in the zone name "East Harlem North" which was the drop off zone that had the largest tip?

Note: it's tip , not trip

We need the name of the zone, not the ID.

Yorkville West
JFK Airport
East Harlem North
East Harlem South

SELECT SUM(tip_amount), dotz."Zone"
FROM green_taxi_trips
INNER JOIN taxi_zones dotz ON dotz."LocationID" = green_taxi_trips."DOLocationID"
INNER JOIN taxi_zones pu ON pu."LocationID" = green_taxi_trips."PULocationID"
WHERE DATE(lpep_pickup_datetime) BETWEEN '2019-10-01' AND '2019-10-31'
AND pu."Zone" = 'East Harlem North'
GROUP BY dotz."Zone"
ORDER BY SUM(tip_amount) DESC
LIMIT 3;

Look like the answer is Upper East Side North, which is not in the option

"""