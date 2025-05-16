from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, expr, when

# Configuración explícita de SparkSession con bucket 
spark = SparkSession.builder \
    .appName("GCP-Batch-ETL") \
    .config("spark.jars", "gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.36.1.jar") \
    .config("spark.sql.legacy.timeParserPolicy", "LEGACY") \
    .config("temporaryGcsBucket", "auto-sales-bigdata") \
    .getOrCreate()

# Leer CSV con inferSchema automático
df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv("gs://auto-sales-bigdata/autodata.csv")

# Transformaciones
df = df.withColumn("ORDERDATE", to_date(col("ORDERDATE"), "dd/MM/yyyy")) \
    .withColumn("TOTAL_ORDER_VALUE", col("QUANTITYORDERED") * col("PRICEEACH")) \
    .withColumn("DEAL_CATEGORY",
        when(col("DEALSIZE") == "Small", "Pequeña")
        .when(col("DEALSIZE") == "Medium", "Mediana")
        .when(col("DEALSIZE") == "Large", "Grande")
        .otherwise("Desconocida")
    )

# Guardar en BigQuery con particionamiento
df.write.format("bigquery") \
    .option("table", "bigdata-batch-demo:autodataset.sales_processed") \
    .option("partitionField", "ORDERDATE") \
    .option("clusteredFields", "DEAL_CATEGORY") \
    .mode("overwrite") \
    .save()

# Mostrar métricas
print(f"Filas procesadas: {df.count()}")
df.show(5, truncate=False)