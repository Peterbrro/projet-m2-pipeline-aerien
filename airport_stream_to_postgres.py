from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, col
from pyspark.sql.types import StringType, IntegerType, DoubleType

# -------------------------------
# 1. Initialiser Spark
# -------------------------------
spark = SparkSession.builder \
    .appName("CSV_to_Postgres_Typed") \
    .config("spark.jars.packages", "org.postgresql:postgresql:42.7.3") \
    .getOrCreate()

# -------------------------------
# 2. Lire le CSV
# -------------------------------
csv_file = "/opt/spark-apps/output/airports.csv"
df = spark.read.option("header", "true").csv(csv_file)

print("✅ Aperçu des données CSV :")
df.show(5)

# -------------------------------
# 3. Harmoniser les noms de colonnes
# -------------------------------
df = df \
    .withColumnRenamed("airport_id", "id") \
    .withColumnRenamed("longitude", "lon") \
    .withColumnRenamed("latitude", "lat") \
    .withColumnRenamed("elevation_value", "elevation")

# Ajouter la colonne 'icao' si elle n'existe pas
if 'icao' not in df.columns:
    df = df.withColumn("icao", lit(None).cast(StringType()))

# -------------------------------
# 4. Caster les colonnes aux types PostgreSQL
# -------------------------------
df = df \
    .withColumn("id", col("id").cast(IntegerType())) \
    .withColumn("name", col("name").cast(StringType())) \
    .withColumn("icao", col("icao").cast(StringType())) \
    .withColumn("type", col("type").cast(IntegerType())) \
    .withColumn("country", col("country").cast(StringType())) \
    .withColumn("lon", col("lon").cast(DoubleType())) \
    .withColumn("lat", col("lat").cast(DoubleType())) \
    .withColumn("elevation", col("elevation").cast(DoubleType()))

# Réordonner les colonnes pour correspondre à la table Postgres
df = df.select("id", "name", "icao", "type", "country", "lon", "lat", "elevation")

# -------------------------------
# 5. Écriture dans PostgreSQL
# -------------------------------
# Nouvelle table pour éviter les problèmes de types
df.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://postgres:5432/mydb") \
    .option("dbtable", "aeroports") \
    .option("user", "admin") \
    .option("password", "admin") \
    .option("driver", "org.postgresql.Driver") \
    .mode("overwrite") \
    .save()

print("✅ CSV écrit dans Postgres dans la table 'aeroports' avec succès !")
