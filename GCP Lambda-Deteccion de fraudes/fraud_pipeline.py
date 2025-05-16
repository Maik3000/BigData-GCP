#!/usr/bin/env python3
import json
import logging
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, SetupOptions
from apache_beam.io.gcp.pubsub import ReadFromPubSub
from apache_beam.io.gcp.bigquery import WriteToBigQuery, BigQueryDisposition
from google.cloud import pubsub_v1
from datetime import datetime

# --- 1. Definición de opciones personalizadas ----
class FraudOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument(
            '--input_topic',
            required=True,
            help='Full Pub/Sub topic to read from, e.g. projects/.../topics/transactions-topic')
        parser.add_argument(
            '--alert_topic',
            required=True,
            help='Full Pub/Sub topic where to publish fraud alerts')
        parser.add_argument(
            '--output_table',
            required=True,
            help='BigQuery table to write all transactions: PROJECT:DATASET.TABLE')

# --- 2. Lógica de detección y transformaciones ----
HIGH_RISK_COUNTRIES = {'North Korea', 'Iran', 'Russia'}

def is_suspicious(event):
    try:
        if event.get('isSuspicious') in (True, 'TRUE', 'true'):
            return True
        if float(event.get('amount', 0)) > 10000:
            return True
        if event.get('country') in HIGH_RISK_COUNTRIES:
            return True
    except Exception as e:
        logging.warning(f"Error evaluando transacción sospechosa: {e}")
    return False

def publish_alert(event, alert_topic, publisher):
    data = {
        "transactionId": event.get('transactionId'),
        "userId":        event.get('userId'),
        "amount":        event.get('amount'),
        "timestamp":     event.get('timestamp'),
        "country":       event.get('country'),
        "reason":        ("flagged" if event.get('isSuspicious') in (True, 'TRUE', 'true')
                          else "high_amount" if float(event.get('amount',0)) > 10000
                          else "risky_country"),
        "detectedAt":    datetime.utcnow().isoformat() + "Z"
    }

    try:
        publisher.publish(alert_topic, json.dumps(data).encode('utf-8'))
        logging.info(f"📤 Alerta enviada: {data}")
    except Exception as e:
        logging.error(f"❌ Error publicando alerta: {e}")

    return event  # Passthrough

def transform_for_bq(event):
    return {
        "transactionId": event.get('transactionId'),
        "userId":        event.get('userId'),
        "amount":        float(event.get('amount', 0)),
        "timestamp":     event.get('timestamp'),
        "country":       event.get('country'),
        "cardholderId":  event.get('cardholderId'),
        "isSuspicious":  is_suspicious(event)
    }

def safe_parse(message):
    try:
        return json.loads(message.decode("utf-8"))
    except Exception as e:
        logging.error(f"❌ JSON mal formado: {e}")
        return None

TABLE_SCHEMA = (
    "transactionId:STRING,"
    "userId:STRING,"
    "amount:FLOAT,"
    "timestamp:STRING,"
    "country:STRING,"
    "cardholderId:STRING,"
    "isSuspicious:BOOLEAN"
)

# --- 3. Definición del pipeline ----
def run():
    opts = PipelineOptions().view_as(FraudOptions)
    opts.view_as(SetupOptions).save_main_session = True

    input_topic  = opts.input_topic
    alert_topic  = opts.alert_topic
    output_table = opts.output_table

    publisher = pubsub_v1.PublisherClient()

    with beam.Pipeline(options=opts) as p:
        transactions = (
            p
            | "LeerPubSub" >> ReadFromPubSub(topic=input_topic).with_output_types(bytes)
            | "ParsearJSON" >> beam.Map(safe_parse)
            | "FiltrarNulos" >> beam.Filter(lambda x: x is not None)
        )

        _ = (
            transactions
            | "FiltrarSospechosas" >> beam.Filter(is_suspicious)
            | "PublicarAlertas" >> beam.Map(lambda evt: publish_alert(evt, alert_topic, publisher))
        )

        _ = (
            transactions
            | "TransformarBQ" >> beam.Map(transform_for_bq)
            | "EscribirBQ" >> WriteToBigQuery(
                  output_table,
                  schema=TABLE_SCHEMA,
                  write_disposition=BigQueryDisposition.WRITE_APPEND,
                  create_disposition=BigQueryDisposition.CREATE_IF_NEEDED
              )
        )

if __name__ == '_main_':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    run()