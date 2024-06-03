import os
from dotenv import load_dotenv
import requests
import json
import psycopg2
import pandas as pd
from datetime import datetime

# Cargar variables de entorno desde el .env
load_dotenv()

redshift_config = {
    'host': os.getenv('REDSHIFT_HOST'),
    'database': os.getenv('REDSHIFT_DATABASE'),
    'user': os.getenv('REDSHIFT_USER'),
    'password': os.getenv('REDSHIFT_PASSWORD'),
    'port': os.getenv('REDSHIFT_PORT')
}

twitch_config = {
    'client_id': os.getenv('TWITCH_CLIENT_ID'),
    'client_secret': os.getenv('TWITCH_CLIENT_SECRET')
}

def obtener_token():
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': twitch_config['client_id'],
        'client_secret': twitch_config['client_secret'],
        'grant_type': 'client_credentials'
    }

    response = requests.post(url, data=params)

    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print(f'Error al obtener el token de acceso: {response.status_code}')
        return None

def extraer_datos():
    access_token = obtener_token()

    if access_token:
        url = 'https://api.twitch.tv/helix/streams'
        params = {'first': 100}  

        headers = {
            'Client-Id': twitch_config['client_id'],
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()

            # Guardar en JSON
            with open('twitch_data.json', 'w') as json_file:
                json.dump(data, json_file)

            # Crear DataFrame a partir de los datos extraídos
            streams = []
            for stream in data['data']:
                streams.append({
                    'stream_id': stream['id'],
                    'user_id': stream['user_id'],
                    'user_name': stream['user_name'],
                    'game_id': stream['game_id'],
                    'type': stream['type'],
                    'title': stream['title'],
                    'viewer_count': stream['viewer_count'],
                    'started_at': stream['started_at'],
                    'language': stream['language'],
                    'thumbnail_url': stream.get('thumbnail_url', None),
                    'channel_url': f"https://www.twitch.tv/{stream['user_name']}",
                    'ingestion_time': datetime.now().isoformat(),
                    'PRIMARY_KEY': f"{stream['id']}_{stream['user_id']}"
                })

            df = pd.DataFrame(streams)
            
            # Exportar los datos a un  CSV
            df.to_csv('twitch_data.csv', index=False)

            # Conexión con Redshift
            conn = psycopg2.connect(**redshift_config)
            cur = conn.cursor()

            # Eliminar tabla si existe
            cur.execute("DROP TABLE IF EXISTS twitch_streams;")

            # Crear tabla si no existe
            cur.execute("""
            CREATE TABLE IF NOT EXISTS twitch_streams (
                stream_id VARCHAR(255),
                user_id VARCHAR(255),
                user_name VARCHAR(255),
                game_id VARCHAR(255),
                type VARCHAR(50),
                title VARCHAR(500),
                viewer_count INT,
                started_at TIMESTAMP,
                language VARCHAR(50),
                thumbnail_url VARCHAR(500),
                channel_url VARCHAR(500),
                ingestion_time TIMESTAMP,
                PRIMARY KEY (stream_id, user_id),
                PRIMARY_KEY VARCHAR(255)
            );
            """)

            # Insertar datos en la tabla
            for _, row in df.iterrows():
                cur.execute("""
                INSERT INTO twitch_streams (stream_id, user_id, user_name, game_id, type, title, viewer_count, started_at, language, thumbnail_url, channel_url, ingestion_time, PRIMARY_KEY) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, 
                (
                    row['stream_id'], row['user_id'], row['user_name'], row['game_id'], row['type'], 
                    row['title'], row['viewer_count'], row['started_at'], row['language'], 
                    row['thumbnail_url'], row['channel_url'], row['ingestion_time'], row['PRIMARY_KEY']
                ))

            # Confirmar cambios, close cursor y conexion
            conn.commit()
            cur.close()
            conn.close()

        else:
            print(f'Error al realizar la solicitud: {response.status_code}')
    else:
        print('No se pudo obtener el token de acceso.')

if __name__ == "__main__":
    # Extraer y cargar datos en Redshift
    extraer_datos()

    # Cargar datos de Redshift en un DataFrame de Pandas
    conn = psycopg2.connect(**redshift_config)
    sql_query = 'SELECT * FROM twitch_streams'
    df = pd.read_sql(sql_query, conn)
    conn.close()

    # Mostrar los primeros registros del DataFrame para checkear si esta funcionando ok.
    print(df.head())
