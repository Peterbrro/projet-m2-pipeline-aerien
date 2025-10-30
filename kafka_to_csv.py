from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, explode
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, ArrayType

# -----------------------------
# 1️⃣ Spark Session
# -----------------------------
spark = (
    SparkSession.builder
    .appName("KafkaToCSV")
    .config("spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# -----------------------------
# 2️⃣ Lecture depuis Kafka
# -----------------------------
df_raw = (
    spark.read
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("subscribe", "quickstart")
    .option("startingOffsets", "earliest")
    .load()
)

df_string = df_raw.selectExpr("CAST(value AS STRING) as json_data")

# -----------------------------
# 3️⃣ Schéma JSON
# -----------------------------
airport_schema = StructType([
    StructField("_id", StringType(), True),
    StructField("name", StringType(), True),
    StructField("type", IntegerType(), True),
    StructField("country", StringType(), True),
    StructField("geometry", StructType([
        StructField("type", StringType(), True),
        StructField("coordinates", ArrayType(DoubleType()), True)
    ]), True),
    StructField("elevation", StructType([
        StructField("value", DoubleType(), True),
        StructField("unit", IntegerType(), True),
        StructField("referenceDatum", IntegerType(), True)
    ]), True)
])

root_schema = StructType([
    StructField("items", ArrayType(airport_schema), True)
])

# -----------------------------
# 4️⃣ Parsing du JSON
# -----------------------------
df_parsed = df_string.select(from_json(col("json_data"), root_schema).alias("data"))
df_exploded = df_parsed.select(explode(col("data.items")).alias("airport"))

df_clean = df_exploded.select(
    col("airport._id").alias("airport_id"),
    col("airport.name").alias("name"),
    col("airport.type").alias("type"),
    col("airport.country").alias("country"),
    col("airport.geometry.coordinates")[0].alias("longitude"),
    col("airport.geometry.coordinates")[1].alias("latitude"),
    col("airport.elevation.value").alias("elevation_value")
)

# -----------------------------
# 5️⃣ Sauvegarde en CSV
# -----------------------------
output_path = "/opt/spark-apps/output/airports.csv"

(
    df_clean.coalesce(1)  # un seul fichier CSV
    .write
    .option("header", "true")
    .mode("overwrite")
    .csv(output_path)
)

print(f"✅ Données exportées dans {output_path}")

spark.stop()
