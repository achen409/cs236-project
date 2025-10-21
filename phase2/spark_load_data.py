from pyspark.sql import SparkSession

# spark session init
spark: SparkSession = SparkSession.builder.config(
    "spark.jars.packages", "org.postgresql:postgresql:42.7.8"
).getOrCreate()

# load CSV files
customer_reservations = spark.read.csv(
    "customer_reservations.csv", header=True, inferSchema=True
)
hotel_booking_cleaned = spark.read.csv(
    "hotel_booking_cleaned.csv", header=True, inferSchema=True
)
all_bookings = spark.read.csv(
    "phase1_output_datasets/all_bookings.csv",
    header=True,
    inferSchema=True,
)

# spark db authentication info
spark_db_url = "jdbc:postgresql://localhost:5432/bookings"
spark_db_properties = {
    "user": "postgres",
    "password": "password",
    "driver": "org.postgresql.Driver",
}

# writing to postgres db
customer_reservations.write.jdbc(
    spark_db_url,
    "customer_reservations",
    properties = spark_db_properties,
)
hotel_booking_cleaned.write.jdbc(
    spark_db_url,
    "hotel_booking",
    properties = spark_db_properties,
)
all_bookings.write.jdbc(
    spark_db_url,
    "all_bookings",
    properties = spark_db_properties,
)
