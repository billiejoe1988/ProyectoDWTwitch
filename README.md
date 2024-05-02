# ProyectoDWTwitch

## Project Description:

The project is an application that retrieves real-time data from the official Twitch API, using Python to access the API and Pandas to work with the data in a DataFrame format. This data is periodically updated and stored in Amazon Redshift for further analysis through SQL queries.

## Functionalities:

1. **Real-time Data Retrieval:** The application can request real-time data from the official Twitch API at any time. This allows access to up-to-date information about users, channels, streams, etc.

2. **Processing with Pandas:** The retrieved data is processed and manipulated using the Pandas library in Python. This enables operations such as filtering, grouping, and calculations on the data efficiently.

3. **Storage in Amazon Redshift:** Once the data has been processed, it is loaded into a table in Amazon Redshift. Redshift is a cloud-based data warehousing service that allows storing large volumes of data scalably and performing SQL queries on them.

## Usage:

1. Clone the project repository from GitHub.
2. Install the necessary dependencies using `pip install -r requirements.txt`.
3. Run the main script `main.py` to request and process data from the Twitch API.
4. Configure the Amazon Redshift access credentials in the configuration file.
5. Run the Redshift loading script to upload the processed data to the corresponding table in Redshift.

## System Requirements:

- Python 3.x
- Internet access to connect to the Twitch API.
- Amazon Redshift access credentials to load the data.

**Note:** It's important to consider the usage limits of the Twitch API to avoid exceeding request quotas. Additionally, scheduling the script executions appropriately is recommended to keep the data in Redshift updated as needed.

This README provides an overview of the project and its main functionalities. For more details on implementation and specific usage of each component, please refer to the detailed documentation in the project repository.
