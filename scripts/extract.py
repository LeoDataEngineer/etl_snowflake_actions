import requests
import pandas as pd
import os


def get_data():
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']
    endpoint_subte = f"https://apitransporte.buenosaires.gob.ar/subtes/forecastGTFS?client_id={client_id}&client_secret={client_secret}"
    try:
        response = requests.get(endpoint_subte)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error al hacer la petición a la API:", response.status_code)
            return None
    except Exception as e:
        print("Error al hacer la petición a la API:", str(e))
        return None

def get_forecast(linea):
    id_linea = linea['ID']
    Route_Id = linea['Linea']['Route_Id']
    Direction_ID = linea['Linea']['Direction_ID']
    start_date = linea['Linea']['start_date']

    forecasts = []
    for estacion in linea['Linea']['Estaciones']:
        stop_name = estacion['stop_name']
        arrival_time = estacion['arrival']['time']
        arrival_delay = estacion['arrival']['delay']
        departure_time = estacion['departure']['time']
        departure_delay = estacion['departure']['delay']

        forecasts.append([id_linea, Route_Id, Direction_ID, start_date, stop_name, arrival_time, arrival_delay, departure_time, departure_delay])

    return forecasts

def create_df(data):
    col = ['id_linea', 'Route_Id', 'Direction_ID', 'start_date', 'stop_name', 'arrival_time', 'arrival_delay', 'departure_time', 'departure_delay']
    df = pd.DataFrame(data, columns=col)
    return df

def get_data_raw():
    response = get_data()
    if response:
        datos = []
        for linea in response['Entity']:
            datos.extend(get_forecast(linea))
        df = create_df(datos)

        df.to_csv('subte_data_raw.csv', index=False)

get_data_raw()
