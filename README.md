# 📊 Proyectos de Big Data en Google Cloud Platform

Este repositorio reúne dos proyectos desarrollados durante el curso de Big Data, enfocados en el diseño y ejecución de arquitecturas de procesamiento de datos en Google Cloud Platform (GCP). Cada proyecto implementa un enfoque distinto: uno en procesamiento por lotes (batch) y otro en procesamiento en tiempo real (streaming), aplicando herramientas modernas para la analítica de datos y detección de fraudes.

---

## 🚗 GCP Batch - Auto Sales

### Descripción
Este proyecto implementa una arquitectura de procesamiento por lotes para transformar y analizar datos de ventas de automóviles. Se construyó un pipeline de ETL utilizando herramientas de GCP, desde la carga de datos en Cloud Storage hasta la visualización de resultados en Looker Studio, pasando por transformación en PySpark y almacenamiento en BigQuery.

### Componentes clave
- **Cloud Storage**: Almacenamiento de archivos CSV.
- **Cloud Data Fusion**: Pipeline visual para ETL sin código.
- **Dataproc (PySpark)**: Transformaciones avanzadas distribuidas.
- **BigQuery**: Consulta y análisis de datos a gran escala.
- **Looker Studio**: Visualización interactiva.

### Objetivo
Evaluar distintas herramientas de GCP para procesamiento por lotes y explorar la eficiencia de transformación con PySpark, integración con BigQuery y visualización de métricas clave de ventas de automóviles.

---

## 🛡️ GCP Lambda - Detección de Fraudes

### Descripción
Este proyecto aborda el problema de detección de fraudes en tiempo real usando una arquitectura Lambda sobre GCP. Los datos se simulan y transmiten en tiempo real mediante Pub/Sub, son procesados por Data Flow, almacenados en BigQuery, analizados con BigQuery ML, y visualizados en Looker Studio.

### Componentes clave
- **Pub/Sub**: Ingesta de datos en streaming.
- **Data Flow**: Procesamiento de la data historica.
- **BigQuery**: Almacenamiento en tablas.
- **BigQuery ML**: Entrenamiento y predicción de modelos de fraude.
- **Looker Studio**: Dashboards en tiempo real.

### Objetivo
Simular un entorno de detección de fraudes financiero en tiempo real, demostrando la capacidad de GCP para procesar eventos conforme llegan y ejecutar modelos de machine learning de forma automática y escalable.

---

## 🎯 Conclusión

Ambos proyectos muestran la versatilidad y potencia de Google Cloud para diferentes necesidades de procesamiento de datos:

- **Batch**: Ideal para cargas programadas y análisis históricos.
- **Streaming (Lambda)**: Enfocado en análisis en tiempo real y respuestas inmediatas.

A través de estas experiencias prácticas, se logró un entendimiento integral de los ecosistemas de Big Data modernos y las mejores prácticas de arquitectura en la nube. Ademas, se logró un entendimiento sobre muchisimos de los servicios que ofrece la misma.

---

## 🔗 Recursos adicionales
- [Documentación de BigQuery](https://cloud.google.com/bigquery)
- [Guía de Cloud Data Fusion](https://cloud.google.com/data-fusion)
- [Dataproc y Apache Spark](https://cloud.google.com/dataproc)
- [Google Cloud Pub/Sub](https://cloud.google.com/pubsub)
- [BigQuery ML](https://cloud.google.com/bigquery-ml)
- [Looker Studio](https://lookerstudio.google.com/)
