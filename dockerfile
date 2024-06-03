# Usar una imagen oficial de Python como base
FROM python:3.8

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Establecer info
LABEL version="1.0"
LABEL author="arbelaiz.dev"

# Puerto 
EXPOSE 8080

# Copiar el archivo requirements.txt y los archivos DAG y ETL a la imagen
COPY requirements.txt .
COPY dags/twitch_dag.py .
COPY twitch_etl.py .

# Instalar las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Especificar el comando a ejecutar al iniciar el contenedor
CMD ["python", "twitch_dag.py"]
