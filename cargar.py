import pandas as pd
import psycopg2
from config import redshift_config

# seleccionar datos de la tabla twitch_streams
sql_query = 'SELECT * FROM twitch_streams'

# conexión con Redshift
conn = psycopg2.connect(**redshift_config)

# Cargar datos DataFrame usando pandas y cerrar conexion
df = pd.read_sql(sql_query, conn)

conn.close()
