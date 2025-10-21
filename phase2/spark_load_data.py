from pyspark.sql import SparkSession

spark: SparkSession = SparkSession.builder.config(
    "spark.jars.packages", "org.postgresql:postgresql:42.7.8"
).getOrCreate()

bookings_df = spark.read.csv(
    "phase1_output_datasets/all_bookings.csv",
    header=True,
    inferSchema=True,
)

bookings_df.write.jdbc(
    "jdbc:postgresql://localhost:5432/bookings",
    "bookings",
    properties={
        "user": "postgres",
        "password": "password",
        "driver": "org.postgresql.Driver",
    },
)
