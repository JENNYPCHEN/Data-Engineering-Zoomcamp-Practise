FROM python:3.9.1

# Install wget to download the CSV file and other necessary packages
RUN apt-get update && apt-get install -y wget && \
    pip install pandas sqlalchemy psycopg2-binary pgcli

WORKDIR /app
COPY ingest_data.py ingest_data.py 

ENTRYPOINT [ "python", "ingest_data.py" ]
