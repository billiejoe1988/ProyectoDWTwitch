from datetime import datetime, timedelta
from airflow import DAG  # type: ignore
from airflow.operators.python_operator import PythonOperator # type: ignore
from airflow.utils.email import send_email # type: ignore
from twitch_etl import obtener_token, extraer_datos

# Argumentos
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1), # feche por si es necesario hacer un backfill
    'email_on_failure': True,  # envío de correo si falla
    'email_on_retry': False,
    'retries': 3,  # 3 intentos 
    'retry_delay': timedelta(minutes=5),  # retardo entre intentos
}

# enviar correo electronico alerta si falla
def task_failure_alert(context):
    """Send email alert on task failure."""
    dag_id = context.get('dag').dag_id
    task_id = context.get('task_instance').task_id
    execution_date = context.get('execution_date')
    log_url = context.get('task_instance').log_url
    email_subject = f"Airflow alert: {dag_id}.{task_id} Failed"
    email_body = f"""
    DAG: {dag_id}<br>
    Task: {task_id}<br>
    Execution Time: {execution_date}<br>
    Log: <a href="{log_url}">Link</a><br>
    """
    send_email('admin@admin.com', email_subject, email_body)

# DAG
dag = DAG(
    'twitch_data_pipeline',
    default_args=default_args,
    description='Un DAG para extraer y cargar datos de Twitch',
    schedule_interval=timedelta(days=1),
)

# Definir token de acceso
get_token_task = PythonOperator(
    task_id='get_twitch_access_token',
    python_callable=obtener_token,
    dag=dag,
    on_failure_callback=task_failure_alert,  # callback por si falla
    retries=default_args['retries'],  # numero de intentos definido arriba
    retry_delay=default_args['retry_delay'],  # retardo entre intentos definido arriba
)

# Extraer los datos
extract_task = PythonOperator(
    task_id='extract_twitch_data',
    python_callable=extraer_datos,
    dag=dag,
    on_failure_callback=task_failure_alert,  # agrega callback por si falla
    retries=default_args['retries'],  # numero de reintentos definido arriba
    retry_delay=default_args['retry_delay'],  # retardo entre intentos definido arriba
)