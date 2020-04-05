from flask import Flask, render_template, url_for, request, redirect, jsonify, config
import json
import requests
import numpy as np
from weather import *
from model import *
from flask_bootstrap import Bootstrap
app = Flask(__name__)

Bootstrap(app)

@app.route('/',methods=['GET', 'POST'])
def index():
    create_and_train_model()
    return render_template("index.html")

@app.route('/mapa',methods=['GET', 'POST'])
def mapa(): 
    return render_template("Mapa.html" )

@app.route('/mapa_simple',methods=['GET', 'POST'])
def mapa_simple(): 
    return render_template("mapa_simple.html" )

@app.route('/longitudes',methods=['GET', 'POST'])
def Longitudes():
  
    puntosArray = []
    # Using readlines() 
    file1 = open('Longitudes.txt', 'r') 
    Lines = file1.readlines()  
    # Strips the newline character 
    for line in Lines:          
        line = line.rstrip('\n')
        puntoObj = {}        
        latitud = "40.537685"
        longitud = str(line)
        puntoObj['Latitud'] = latitud
        puntoObj['Longitud'] = longitud    
        puntosArray.append(puntoObj)  
    return jsonify(puntosArray)

@app.route('/givemelocation',methods=['POST'])
def Getlocation(): 
   
    localizacion = request.json
    #print("la localizacion es la siguiente "+str(localizacion))
    api_key = "13322246a8ad4613a0ca2608f8942168"
    base_url = 'https://api.weatherbit.io/v2.0/forecast/daily'                
    lat = localizacion['latitud']
    lon = localizacion['longitud']

    base_urlprovince = 'https://maps.googleapis.com/maps/api/geocode/json'
    paramsprovince = { 
        'latlng':str(lat)+','+str(lon),
        'key':'AIzaSyAK5rkIpH-otp0e2JMOqZ-t7D8Z1vRKkYw'                 
    }
    headersprovince = {
        'cache-control': "no-cache"
    }
    responseprovince = requests.request('GET', base_urlprovince, params=paramsprovince, headers=headersprovince)
    respuesta = responseprovince.json()   
    for dataprovince in respuesta['results']:
        provincia = dataprovince['address_components'][2]['long_name']
        comunidad = dataprovince['address_components'][3]['long_name']
        break

    #print ("provincia: "+provincia)
    #print ("Comunidad autónoma: " + comunidad)

    # params = {            
    #     'lat':lat,
    #     'lon':lon,
    #     'days':'7',
    #     'lang':'es',
    #     'key':api_key
    # }

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
        
    forecast_temperature = tempArray
    temp_provincia, simple_temp_provincia = temperature_data(provincia)




    return 'ok'
    






  
"""def temperature_data(name):
    r, station_code = get_stations(provincia = name.upper())

    api_key = api_key = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJwYWJsbzE2Mjk4QGhvdG1haWwuY29tIiwianRpIjoiZWY3MTZmYTUtZjdjNy00MmY0LWI0ZDEtN2RmOTAyMzA5M2FlIiwiaXNzIjoiQUVNRVQiLCJpYXQiOjE1ODU1NjA3MDUsInVzZXJJZCI6ImVmNzE2ZmE1LWY3YzctNDJmNC1iNGQxLTdkZjkwMjMwOTNhZSIsInJvbGUiOiIifQ.Zn3YOUpHQYrcf4woFBZP0vgzSmxJjlDRFqu9rQfNxwI"
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
    api_key = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJwYWJsbzE2Mjk4QGhvdG1haWwuY29tIiwianRpIjoiZWY3MTZmYTUtZjdjNy00MmY0LWI0ZDEtN2RmOTAyMzA5M2FlIiwiaXNzIjoiQUVNRVQiLCJpYXQiOjE1ODU1NjA3MDUsInVzZXJJZCI6ImVmNzE2ZmE1LWY3YzctNDJmNC1iNGQxLTdkZjkwMjMwOTNhZSIsInJvbGUiOiIifQ.Zn3YOUpHQYrcf4woFBZP0vgzSmxJjlDRFqu9rQfNxwI"
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
    
    return results, results[0]['indicativo']"""

    


if __name__ == '__main__':    

    app.run(host="localhost", port=5000,debug=True, threaded=True)
    
