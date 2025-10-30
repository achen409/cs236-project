# cs236-project
CS236 Project

# Phase 2

## Download Windows Hadoop files

1. Download https://github.com/steveloughran/winutils
2. `setx HADOOP_HOME path\to\winutils\hadoop-3.0.0\`

## Run the PostgreSQL server

```shell
docker run -d --name bookings_db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=bookings -p 5432:5432 postgres
```

## Initialize data tables

```shell
docker cp .\phase2\create_tables.sql bookings_db:/create_tables.sql 
docker exec -it bookings_db psql -U postgres -d bookings -f /create_tables.sql
```

## Run the pyspark script

```shell
spark-submit --packages org.postgresql:postgresql:42.7.8 .\phase2\spark_load_data.py
```

## Access the page

```shell
docker run -p 8080:8080 adminer
```

Adminer will be running on `localhost:8080`; navigate to that on a browser.

Note: running adminer with Docker will not have direct access to localhost - use `host.docker.internal` as the server instead.