import configparser
import requests
import os
import pandas as pd
import numpy as np

config = configparser.ConfigParser()
config.read("../config.ini")
DATA_FOLDER =  os.path.dirname(os.getcwd()) + '/data/'


### v1 of weather.py ###
"""def temperature_data(name):
    r, station_code = get_stations(provincia = name.upper())

    api_key = config['aemet']['api_key']
    base_url = 'https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/2020-01-01T00%3A00%3A00UTC/fechafin/2020-04-03T00%3A00%3A00UTC/estacion/{}'.format(station_code)

    params = {
        'api_key': api_key
    }
    headers = {
        'cache-control': "no-cache"
    }

    response = requests.request('GET', base_url, params=params, headers=headers)

    response_url = response.json()['datos']

    data = requests.request('GET', response_url)
    
    simple_results = np.array([float(value['tmed'].replace(',','.')) for value in data.json()])

    results = {}
    for value in data.json():
        results[value['fecha']] = float(value['tmed'].replace(',','.'))

    return results, simple_results

def get_stations(provincia):
    api_key = config['aemet']['api_key']
    base_url = 'https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones'

    params = {
        'api_key': api_key
    }
    headers = {
        'cache-control': "no-cache"
    }

    response = requests.request('GET', base_url, params=params, headers=headers)

    response_url = response.json()['datos']

    data = requests.request('GET', response_url)

    results = [result for result in data.json() if result['provincia'] == provincia]
    
    return results, results[0]['indicativo']"""
### end ofv1 of weather.py ###

### v2 of weather.py ###
def temperature_data(name):
    r, station_code = get_stations(provincia = name.upper())

    api_key =  config['aemet']['api_key']
    base_url = 'https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/2020-01-01T00%3A00%3A00UTC/fechafin/2020-04-03T00%3A00%3A00UTC/estacion/{}'.format(station_code)

    params = {
        'api_key': api_key
    }
    headers = {
        'cache-control': "no-cache"
    }

    response = requests.request('GET', base_url, params=params, headers=headers)
    #print("respuesta datos provincia")
    #print(response)
    response_url = response.json()['datos']

    data = requests.request('GET', response_url)
    
    simple_results = np.array([float(value['tmed'].replace(',','.')) for value in data.json()])

    results = {}
    for value in data.json():
        results[value['fecha']] = float(value['tmed'].replace(',','.'))

    return results, simple_results

def get_stations(provincia):
    api_key = config['aemet']['api_key']
    base_url = 'https://opendata.aemet.es/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones'

    params = {
        'api_key': api_key
    }
    headers = {
        'cache-control': "no-cache"
    }

    response = requests.request('GET', base_url, params=params, headers=headers)
    #print("imprimiendo respuesta estaciones provincia")
    #print(response)
    response_url = response.json()['datos']

    data = requests.request('GET', response_url)

    #print("imprimiendo data")
    #print(data)
    results = [result for result in data.json() if result['provincia'] == provincia]
    
    return results, results[0]['indicativo']
### end of v2 of weather.py ###

def read_weather_csv(filename):
    fname = DATA_FOLDER + filename

    df = pd.read_csv(fname)

    tavg = df['TAVG'].to_numpy()
    dates = df['DATE']

    # Fahrenhei a celsius
    tavg_celsius = [round(((t - 32) * 5)/9,2) for t in tavg]
    simple_results = np.array(tavg_celsius)

    results = {}
    for i in range(len(dates)):
        results[dates[i]] = tavg_celsius[i]

    return results, simple_results

# obtencion de array de temperaturas de los proximos 7 dias 
def getProvincia (lat,lon):

    base_urlprovince = 'https://maps.googleapis.com/maps/api/geocode/json'
    paramsprovince = { 
        'latlng':str(lat)+','+str(lon),
        'key': config['google']['api_key']                 
    }
    headersprovince = {
        'cache-control': "no-cache"
    }
    responseprovince = requests.request('GET', base_urlprovince, params=paramsprovince, headers=headersprovince)
    respuesta = responseprovince.json() 
    provincia = ""
    for dataprovince in respuesta['results']: 
        provincia = dataprovince['address_components'][len(dataprovince)-3 ]['long_name']
        comunidad = dataprovince['address_components'][len(dataprovince)-2]['long_name']
        comunidadformateada = formalizarCCAA(comunidad)
        break

    return provincia
def getArrayTemp(provincia):   
    
    api_key = config['weatherbit']['api_key']
    base_url = 'https://api.weatherbit.io/v2.0/forecast/daily' 

    
    params = { 
        'city':provincia,
        'country':'es',
        'days':'7',
        'key':api_key
    }


    headers = {
        'cache-control': "no-cache"
    }

    response = requests.request('GET', base_url, params=params, headers=headers)
    forecast = response.json()   
    tempArray = []
    for data in forecast['data']:
        tempArray.append(data['temp'])

    return tempArray

#funcion para formalizar las cadenas de las comunidades autonomas.
def formalizarCCAA(comunidad):
    comunidades = ["Andalucía","Aragón","Asturias","Baleares","Canarias","Cantabria","Castilla-La Mancha","Castilla y León","Cataluña","Ceuta","C. Valenciana","Extremadura","Galicia","Madrid","Melilla","Murcia","Navarra","País Vasco","La Rioja"]
    tamanio = len(comunidades)    
    range(0,len(comunidades))  
    encontrado = False
    for x in range(0,len(comunidades)):
        if comunidad in comunidades[x]:
            if comunidad in "Comunidad Valenciana":
                comunidadformateada = "C. Valenciana"
            else:
                comunidadformateada =  comunidades[x] 
            
            encontrado = True
        else: 
            if encontrado  == False :
                comunidadformateada  = "empty"
        
    return comunidadformateada
