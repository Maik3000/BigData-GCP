from google.cloud import pubsub_v1
import json
import random
import time
import csv

# Cambia esto por tu ID de proyecto
project_id = "proyecto-final-big-data-459203"
topic_id = "transactions-stream"

# Configurar cliente de Pub/Sub
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

with open('streamingTransactions.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data = json.dumps(row).encode("utf-8")
        future = publisher.publish(topic_path, data=data)
        print(f"Publicado: {future.result()}")
        time.sleep(0.5)  # simula streaming en tiempo real

