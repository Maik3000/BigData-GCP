import json
import logging
import signal
import sys

from google.cloud import pubsub_v1
from google.cloud import bigquery

# Configuración fija
projectId      = 'proyecto-final-big-data-459203'
subscriptionId = 'testSub'
datasetId      = 'finsafe_dataset'
tableId        = 'deteccionFraude'

# Cliente de BigQuery (global)
bq_client = bigquery.Client(project=projectId)
table_ref = bq_client.dataset(datasetId).table(tableId)

# Lista de países de alto riesgo
HIGH_RISK_COUNTRIES = {'GT'}

def processMessage(message):
    try:
        payload = json.loads(message.data.decode('utf-8'))
        txnId    = payload.get('transactionId')
        userId   = payload.get('userId')
        amount   = float(payload.get('amount', 0))
        country  = payload.get('country', '').strip()
        isSourceFlag = payload.get('isSuspicious') in (True, 'TRUE', 'true')

        logging.info(
            f"💳 Transacción recibida | txnId={txnId} | userId={userId} | "
            f"amount={amount} | country={country} | sourceFlag={isSourceFlag}"
        )

        # Alerta si hay sospecha
        if isSourceFlag:
            logging.warning('🚨 ALERTA: sistema origen marcó como sospechosa')
        elif amount > 10000:
            logging.warning('⚠ ALERTA: monto elevado')
        elif country in HIGH_RISK_COUNTRIES:
            logging.warning('⚠ ALERTA: país de alto riesgo')
        else:
            logging.info('✅ Transacción normal')

        # Guardar en BigQuery
        row = {
            "transactionId": txnId,
            "userId": userId,
            "amount": amount,
            "country": country,
            "isSuspicious": isSourceFlag
        }
        errors = bq_client.insert_rows_json(table_ref, [row])
        if errors:
            logging.error(f'❌ Error al guardar en BigQuery: {errors}')
        else:
            logging.info('📝 Transacción guardada en BigQuery')

        message.ack()
    except Exception:
        logging.exception('❌ Error procesando mensaje')
        message.nack()

def main():
    # Configura logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s'
    )

    subscriber = pubsub_v1.SubscriberClient()
    subscriptionPath = subscriber.subscription_path(projectId, subscriptionId)
    streamingFuture = subscriber.subscribe(subscriptionPath, callback=processMessage)

    logging.info(f'🔍 Escuchando en {subscriptionPath}…')

    # Manejador de cierre limpio
    def shutdown(signum, frame):
        logging.info('🛑 Deteniendo consumidor...')
        streamingFuture.cancel()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    streamingFuture.result()

if __name__ == '__main__':
    main()