from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

try:
    # spark session init
    spark = (
        SparkSession.builder
        .appName("LoadDataToPostgres")
        .master("local[*]")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .config("spark.driver.host", "127.0.0.1")
        .config("spark.shuffle.push.enabled", "false")
        .config("spark.jars.packages", "org.postgresql:postgresql:42.7.8")
        .getOrCreate()
    )

    # schemas
    customer_reservations_schema = StructType([
        StructField("booking_id", StringType(), False),
        StructField("stays_in_weekend_nights", IntegerType(), False),
        StructField("stays_in_week_nights", IntegerType(), False),
        StructField("lead_time", IntegerType(), False),
        StructField("arrival_year", IntegerType(), False),
        StructField("arrival_month", IntegerType(), False),
        StructField("arrival_day", IntegerType(), False),
        StructField("market_segment_type", StringType(), False),
        StructField("avg_price_per_room", DoubleType(), False),
        StructField("booking_status", IntegerType(), False),
    ])
    hotel_booking_schema = StructType([
        StructField("hotel", StringType(), False),
        StructField("booking_status", IntegerType(), False),
        StructField("lead_time", IntegerType(), False),
        StructField("arrival_year", IntegerType(), False),
        StructField("arrival_month", IntegerType(), False),
        StructField("arrival_date_week_number", IntegerType(), False),
        StructField("arrival_day", IntegerType(), False),
        StructField("stays_in_weekend_nights", IntegerType(), False),
        StructField("stays_in_week_nights", IntegerType(), False),
        StructField("market_segment_type", StringType(), False),
        StructField("country", StringType(), False),
        StructField("avg_price_per_room", DoubleType(), False),
        StructField("email", StringType(), False),
    ])
    all_bookings_schema = StructType([
        StructField("stays_in_weekend_nights", IntegerType(), False),
        StructField("stays_in_week_nights", IntegerType(), False),
        StructField("lead_time", IntegerType(), False),
        StructField("arrival_year", IntegerType(), False),
        StructField("arrival_month", IntegerType(), False),
        StructField("arrival_day", IntegerType(), False),
        StructField("market_segment_type", StringType(), False),
        StructField("avg_price_per_room", DoubleType(), False),
        StructField("booking_status", IntegerType(), False),
        StructField("email", StringType(), True),
        StructField("booking_id", StringType(), True),
    ])

    # load CSV files

    # customer_reservations = spark.read.format("csv").schema(customer_reservations_schema).option("header", True).load("phase1_output_datasets/customer_reservations.csv")
    # hotel_booking = spark.read.format("csv").schema(hotel_booking_schema).option("header", True).load("phase1_output_datasets/hotel_booking_cleaned.csv")
    # all_bookings = spark.read.format("csv").schema(all_bookings_schema).option("header", True).load("phase1_output_datasets/all_bookings.csv")

    customer_reservations = spark.read.csv(
        "phase1_output_datasets/customer_reservations.csv", header=True, schema=customer_reservations_schema
    )
    hotel_booking = spark.read.csv(
        "phase1_output_datasets/hotel_booking_cleaned.csv", header=True, schema=hotel_booking_schema
    )
    all_bookings = spark.read.csv(
        "phase1_output_datasets/all_bookings.csv",
        header=True,
        schema=all_bookings_schema
    )

    # spark db authentication info
    spark_db_url = "jdbc:postgresql://localhost:5432/bookings"
    spark_db_properties = {
        "user": "postgres",
        "password": "password",
        "driver": "org.postgresql.Driver",
    }

    # writing to postgres db
    customer_reservations.write.option("truncate", "true").jdbc(
        spark_db_url,
        "customer_reservations",
        properties = spark_db_properties,
        mode="overwrite"
    )
    hotel_booking.write.option("truncate", "true").jdbc(
        spark_db_url,
        "hotel_booking",
        properties = spark_db_properties,
        mode="overwrite"
    )
    all_bookings.write.option("truncate", "true").jdbc(
        spark_db_url,
        "all_bookings",
        properties = spark_db_properties,
        mode="overwrite"
    )

finally:
    if spark is not None:
        spark.stop()
