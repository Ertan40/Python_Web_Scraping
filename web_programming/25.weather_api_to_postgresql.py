from datetime import datetime
import requests
from sqlalchemy import create_engine, Table, Column, Integer, String, Date, MetaData, Float
from sqlalchemy.exc import SQLAlchemyError
import psycopg2
import pandas as pd


# Function to fetch data from Weather API
def fetch_weather_data(**kwargs):
    # url = kwargs['url']
    url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': 'London',
        'APPID': 'Your-API-key-goes-here',
        'units': 'metric'
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Raise an exception if the request fails
        data = response.json()
        return data
    except requests.exceptions.RequestException as error:
        print(f"An error occurred: {str(error)}")
        return None


def transform_weather_data(weather_data):

    transformed_data = {
        'lon': weather_data['coord']['lon'],
        'lat': weather_data['coord']['lat'],
        'temperature': weather_data['main']['temp'],
        'temp_min': weather_data['main']['temp_min'],
        'temp_max': weather_data['main']['temp_max'],
        'wind_speed': weather_data['wind']['speed'],
        'description': weather_data['weather'][0]['description'],
        'city': weather_data['name'],
        'country': weather_data['sys']['country'],
        'upload_date': datetime.utcnow().date()
    }
    return transformed_data


def load_weather_data(data_transformed):
    """Load transformed data into PostgreSQL"""
    # convert to dataframe
    df = pd.DataFrame([data_transformed])
    try:
        # Create SQLAlchemy engine
        create_engine('dialect+driver://username:password@host:port/database')

        # Define table metadata
        metadata = MetaData()

        weather_table = Table(
            'weather', metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('lon', Float),
            Column('lat', Float),
            Column('temperature', Float),
            Column('temp_min', Float),
            Column('temp_max', Float),
            Column('wind_speed', Float),
            Column('description', String(30)),
            Column('city', String(20)),
            Column('country', String(10)),
            Column('upload_date', Date),
        )
        # Create the table if it doesn't exist
        metadata.create_all(engine)

        # # Insert data into the table
        df.to_sql('weather', con=engine, if_exists='append', index=False)
        # df.to_sql('weather', con=engine, if_exists='append', index=False, method='multi')

        print("Data imported successfully into PostgreSQL database.")

    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")


# testing
if __name__ == "__main__":
    weather_data = fetch_weather_data()
    if weather_data:
        transformed_data = transform_weather_data(weather_data)
        load_weather_data(transformed_data)
