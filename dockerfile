# Uso la base oficial de Python
FROM python:3.9-slim

ENV AIRFLOW_HOME=/opt/airflow

# Configuro el directorio de trabajo
WORKDIR $AIRFLOW_HOME

# Establecer info
LABEL version="1.0"
LABEL author="arbelaiz.dev"

# Copiar el archivo requirements.txt y los archivos DAG y ETL a la imagen
COPY requirements.txt .
COPY dags/twitch_dag.py .
COPY twitch_etl.py .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto para Airflow UI
EXPOSE 8080

# Copio los archivos DAG al directorio de Airflow
COPY ./dags/ $AIRFLOW_HOME/dags/

# Especificar el comando a ejecutar al iniciar el contenedor
CMD ["airflow webserver & airflow scheduler", "-p", "8080"]
