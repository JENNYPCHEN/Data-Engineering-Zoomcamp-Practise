# Docker and SQL Questions

## Question 1. Understanding Docker First Run

Run Docker with the `python:3.12.8` image in an interactive mode, using the entrypoint `bash`.

### Steps:
1. Create a `Dockerfile` with the following content:

    ```dockerfile
    FROM python:3.12.8
    
    ENTRYPOINT ['bash']
    ```

2. Build the image with the following command (replace `my_python_image` with your preferred name):

    ```sh
    docker build -t my_python_image .
    ```

3. Run the image with the following command:

    ```sh
    docker run -it my_python_image
    ```

4. Check the pip version with:

    ```sh
    pip -V
    ```

#### Answer:
```
pip 24.3.1 from /usr/local/python/3.12.1/lib/python3.12/site-packages/pip (python 3.12)
```

---

## Question 2. Understanding Docker Networking and Docker Compose

Given the following `docker-compose.yaml`, what is the hostname and port that pgAdmin should use to connect to the Postgres database?

```yaml
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
```

#### Answer:
**Hostname:** `postgres`  
**Port:** `5433`

---

## Prepare Postgres

### Steps:
1. Set up the `Dockerfile`:

    ```dockerfile
    FROM python:3.9.1
    
    # Install wget to download the CSV file and other necessary packages
    RUN apt-get update && apt-get install -y wget && \
        pip install pandas sqlalchemy psycopg2-binary pgcli
    
    WORKDIR /app
    COPY ingest_data.py ingest_data.py 
    
    ENTRYPOINT [ "python", "ingest_data.py" ]
    ```

2. Create the `ingest_data.py` file.
3. Create the `docker-compose.yaml` file.
4. Build the image.
5. Run the image.
6. Run Docker Compose.
7. Register the server in pgAdmin.

To solve the `pgAdmin` sessions permission issue, use the following command:

```sh
mkdir -p ./data_pgadmin/sessions
sudo chown -R 5050:5050 ./data_pgadmin
```

---

## Question 3. Trip Segmentation Count

For trips between October 1st, 2019 (inclusive) and November 1st, 2019 (exclusive), how many trips occurred within each distance range?

```sql
SELECT
    SUM(CASE WHEN trip_distance <= 1 THEN 1 ELSE 0 END) AS "Up to 1 mile",
    SUM(CASE WHEN trip_distance > 1 AND trip_distance <= 3 THEN 1 ELSE 0 END) AS "1 to 3 miles",
    SUM(CASE WHEN trip_distance > 3 AND trip_distance <= 7 THEN 1 ELSE 0 END) AS "3 to 7 miles",
    SUM(CASE WHEN trip_distance > 7 AND trip_distance <= 10 THEN 1 ELSE 0 END) AS "7 to 10 miles",
    SUM(CASE WHEN trip_distance > 10 THEN 1 ELSE 0 END) AS "Over 10 miles"
FROM green_taxi_trips
WHERE lpep_pickup_datetime >= '2019-10-01' AND lpep_pickup_datetime < '2019-11-01'
and lpep_dropoff_datetime >= '2019-10-01' AND lpep_dropoff_datetime < '2019-11-01';
```

#### Answer:
```
99999   184243  82536   17013   16021
```

---

## Question 4. Longest Trip for Each Day

Find the longest trip distance for each given day.

```sql
SELECT
    DATE(lpep_pickup_datetime) AS pickup_date,
    MAX(trip_distance) AS longest_trip_distance
FROM green_taxi_trips
WHERE DATE(lpep_pickup_datetime) IN ('2019-10-11', '2019-10-24', '2019-10-26', '2019-10-31')
GROUP BY pickup_date
ORDER BY pickup_date;
```

#### Answer:
```
2019-10-31    515.89
```

---

## Question 5. Three Biggest Pickup Zones

Find the top pickup locations with over 13,000 in `total_amount` for `2019-10-18`.

```sql
SELECT taxi_zones."Zone",count(taxi_zones."Zone")
FROM green_taxi_trips
join taxi_zones on taxi_zones."LocationID" =green_taxi_trips."PULocationID"
WHERE DATE(lpep_pickup_datetime) = '2019-10-18'
and total_amount>13
GROUP BY taxi_zones."Zone"
order by count(taxi_zones."Zone") desc
limit 3;
```

#### Answer:
```
East Harlem North, East Harlem South, Morningside Height
```

---

## Question 6. Largest Tip

Find the drop-off zone with the largest tip for passengers picked up in "East Harlem North" in October 2019.

```sql
SELECT tip_amount, dotz."Zone"
FROM green_taxi_trips
INNER JOIN taxi_zones dotz ON dotz."LocationID" = green_taxi_trips."DOLocationID"
INNER JOIN taxi_zones pu ON pu."LocationID" = green_taxi_trips."PULocationID"
WHERE DATE(lpep_pickup_datetime) BETWEEN '2019-10-01' AND '2019-10-31'
AND pu."Zone" = 'East Harlem North'
ORDER BY tip_amount DESC
LIMIT 3;
```

#### Answer:
```
JFK Airport
```
## Question 7. Terraform Workflow
```
Which of the following sequences, respectively, describes the workflow for:

Downloading the provider plugins and setting up backend,
Generating proposed changes and auto-executing the plan
Remove all resources managed by terraform`
```
#### Answer:
```
terraform init, terraform apply -auto-approve, terraform destroy
```


