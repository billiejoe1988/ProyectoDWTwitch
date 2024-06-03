from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator 
from twitch_etl import obtener_token, extraer_datos

# Definir los argumentos por defecto del DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Definir el DAG
dag = DAG(
    'twitch_data_pipeline',
    default_args=default_args,
    description='Un DAG para extraer y cargar datos de Twitch',
    schedule_interval=timedelta(days=1),
)

# Definir la tarea para obtener el token de acceso
get_token_task = PythonOperator(
    task_id='get_twitch_access_token',
    python_callable=obtener_token,
    dag=dag,
)

# Definir la tarea para extraer los datos
extract_task = PythonOperator(
    task_id='extract_twitch_data',
    python_callable=extraer_datos,
    dag=dag,
)

# Establecer la dependencia entre las tareas
get_token_task >> extract_task
