﻿# ProyectoDWTwitch

## Descripción del Proyecto

El proyecto consiste en una aplicación que recupera datos en tiempo real desde la API oficial de Twitch. Utiliza Python para acceder a la API y Pandas para trabajar con los datos en formato DataFrame. Estos datos se actualizan periódicamente y se almacenan en Amazon Redshift para análisis adicional a través de consultas SQL.

## Funcionalidades

1. **Recuperación de Datos en Tiempo Real:** La aplicación puede solicitar datos en tiempo real desde la API oficial de Twitch en cualquier momento. Esto permite acceder a información actualizada sobre usuarios, canales, transmisiones, etc.

2. **Procesamiento con Pandas:** Los datos recuperados se procesan y manipulan utilizando la biblioteca Pandas en Python. Esto permite realizar operaciones como filtrado, agrupación y cálculos sobre los datos de manera eficiente.

3. **Almacenamiento en Amazon Redshift:** Una vez que los datos han sido procesados, se cargan en una tabla en Amazon Redshift. Redshift es un servicio de almacenamiento de datos en la nube que permite almacenar grandes volúmenes de datos de manera escalable y realizar consultas SQL sobre ellos.

4. **Dockerización:** El proyecto ahora está dockerizado para facilitar el despliegue y la gestión del entorno de desarrollo y producción de manera consistente.

5. **Integración con Apache:** Utiliza Apache para servir la aplicación en un entorno de producción, asegurando una escalabilidad y confiabilidad adecuadas.

## Uso

1. Clona el repositorio del proyecto desde GitHub.
2. Instala las dependencias necesarias utilizando `pip install -r requirements.txt`.
3. Ejecuta el script principal `twitch_etl.py` para solicitar y procesar datos desde la API de Twitch.
4. Configura las credenciales de acceso a Amazon Redshift en el archivo de configuración.
5. Ejecuta el script de carga en Redshift para subir los datos procesados a la tabla correspondiente en Redshift.

6. Por consola, ejecutar docker-compose up --build, levantando las imagenes y pudiendo acceder a Apache Airflow con las credenciales correspondiendos y previa ejecucion de Docker. 

## Requisitos del Sistema

- Python 3.x
- Acceso a Internet para conectarse a la API de Twitch.
- Credenciales de acceso a Amazon Redshift para cargar los datos.
- Docker instalado para el entorno de desarrollo y producción.
- Apache instalado para servir la aplicación en un entorno de producción.

**Nota:** Es importante tener en cuenta los límites de uso de la API de Twitch para evitar exceder las cuotas de solicitud. Además, se recomienda programar las ejecuciones de los scripts de manera adecuada para mantener actualizados los datos en Redshift según sea necesario.

Este README proporciona una visión general del proyecto y sus principales funcionalidades. Para obtener más detalles sobre la implementación y el uso específico de cada componente, consulta la documentación detallada en el repositorio del proyecto.
