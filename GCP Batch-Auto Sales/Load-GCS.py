from google.cloud import storage
import pandas as pd
import io

# Configuración inicial
PROJECT_ID = "bigdata-batch-demo"  # Reemplaza con tu ID de proyecto
BUCKET_NAME = "auto-sales-bigdata"  # Nombre del bucket GCS
CREDENTIALS_PATH = "credentials.json"  # Ruta al archivo JSON de credenciales

# 1. Crear cliente de Cloud Storage
def upload_to_gcs(source_file_path, destination_blob_name):
    """Sube un archivo local a GCS."""
    storage_client = storage.Client.from_service_account_json(CREDENTIALS_PATH)
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_path)
    print(f"Archivo {source_file_path} subido a gs://{BUCKET_NAME}/{destination_blob_name}")

# 2. Cargar desde un DataFrame de Pandas (sin archivo local)
def upload_dataframe_to_gcs(df, destination_blob_name, format="csv"):
    """Sube un DataFrame directamente a GCS en formato CSV o Parquet."""
    storage_client = storage.Client.from_service_account_json(CREDENTIALS_PATH)
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)

    if format == "csv":
        csv_data = df.to_csv(index=False)
        blob.upload_from_string(csv_data, content_type="text/csv")
    elif format == "parquet":
        parquet_buffer = io.BytesIO()
        df.to_parquet(parquet_buffer, engine="pyarrow")
        blob.upload_from_string(parquet_buffer.getvalue(), content_type="application/parquet")
    
    print(f"DataFrame subido a gs://{BUCKET_NAME}/{destination_blob_name} como {format.upper()}")

# --- Ejemplos de uso ---
if __name__ == "__main__":
    # Ejemplo 1: Subir un archivo local (CSV, JSON, etc.)
    upload_to_gcs(
        source_file_path="data/subset_limpio.csv",
        destination_blob_name="autodata.csv"  # Ruta dentro del bucket
    )
