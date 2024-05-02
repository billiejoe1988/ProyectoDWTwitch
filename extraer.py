import requests
import json
import psycopg2
from config import twitch_config, redshift_config

def get_access_token():
    url = 'https://id.twitch.tv/oauth2/token?'
    params = {
        'client_id': twitch_config['client_id'],
        'client_secret': twitch_config['client_secret'],
        'grant_type': 'client_credentials'
    }

    # Realizar la solicitud POST para obtener el token de acceso
    response = requests.post(url, data=params)

    if response.status_code == 200:
    # devolver el token de acceso de la respuesta 
        return response.json().get('access_token')
    else:
        print(f'Error al obtener el token de acceso: {response.status_code}')
        return None

def extraer_datos():
    access_token = get_access_token()

    if access_token:
        url = 'https://api.twitch.tv/helix/streams'
        params = {'first': 100}  

        headers = {
            'Client-Id': twitch_config['client_id'],
            'Authorization': f'Bearer {access_token}'
        }

        # Realizar la solicitud GET a la API de Twitch con el access token que sacamos en el auth
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
        # Convertir JSON en diccionario de Python
            data = response.json()

        # Guardar en JSON 
            with open('twitch_data.json', 'w') as json_file:
                json.dump(data, json_file)

        # Establecer conexión con Redshift
            conn = psycopg2.connect(**redshift_config)

        # Cursor consultas SQL
            cur = conn.cursor()

            for stream in data['data']:
                stream_id = stream['id']
                user_id = stream['user_id']
                user_name = stream['user_name']
                game_id = stream['game_id']
                type = stream['type']
                title = stream['title']
                viewer_count = stream['viewer_count']
                started_at = stream['started_at']
                language = stream['language']
                thumbnail_url = stream.get('thumbnail_url', None) 
                tags = stream.get('tag_ids', []) 
                channel_url = f"https://www.twitch.tv/{user_name}"  
                
         # consulta SQL para insertar datos en la tabla
                cur.execute("INSERT INTO twitch_streams (stream_id, user_id, user_name, game_id, type, title, viewer_count, started_at, language, thumbnail_url, tags, channel_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                            (stream_id, user_id, user_name, game_id, type, title, viewer_count, started_at, language, thumbnail_url, tags, channel_url))

        # Confirmar los cambios, cerrar cursor y conexion
            conn.commit()

            cur.close()
            conn.close()
        else:
            print(f'Error al realizar la solicitud: {response.status_code}')
    else:
        print('No se pudo obtener el token de acceso.')

if __name__ == "__main__":
    extraer_datos()
