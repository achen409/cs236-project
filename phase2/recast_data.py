from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# spark session
spark = SparkSession.builder.getOrCreate()

# reading csv
hotel_booking = spark.read.csv(
    "phase1_output_datasets/hotel_booking_cleaned.csv", header=True, inferSchema=True
)
all_bookings = spark.read.csv(
    "phase1_output_datasets/all_bookings.csv", header=True, inferSchema=True
)

# recast month col
hotel_booking_cleaned = hotel_booking.withColumn("arrival_month", col("arrival_month").cast("int"))
all_bookings_cleaned = all_bookings.withColumn("arrival_month", col("arrival_month").cast("int"))

# writing
hotel_booking_cleaned.write.csv(
    "phase1_output_datasets/hotel_booking_cleaned.csv", header=True, mode="overwrite"
)
all_bookings_cleaned.write.csv(
    "phase1_output_datasets/all_bookings.csv", header=True, mode="overwrite"
)