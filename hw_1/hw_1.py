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


"""