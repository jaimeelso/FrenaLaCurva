from flask import Flask, render_template, url_for, request, redirect, jsonify, config
import json
import requests
import numpy as np
from weather import *
from model import *
from data_builder import *
import configparser
from flask_bootstrap import Bootstrap
app = Flask(__name__)

Bootstrap(app)

config = configparser.ConfigParser()
config.read("../config.ini")
training_window = int(config['training_window']['value'])

@app.route('/',methods=['GET', 'POST'])
def index():
    
    return render_template("index.html")

@app.route('/mapa',methods=['GET', 'POST'])
def mapa(): 
    global training_window
    create_and_train_model(training_window=training_window)
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
        provincia = dataprovince['address_components'][len(dataprovince)-3 ]['long_name']
        comunidad = dataprovince['address_components'][len(dataprovince)-2]['long_name']

        break

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

    training_window = int(config['training_window']['value'])

    # Datos de temperatura de la CCAA
    forecast_temperature = np.array(tempArray)
    
    temp_provincia, simple_temp_provincia = temperature_data(provincia)

    # Datos de infectados de la CCAA
    values_infected_provincia, simple_values_infected_provincia= read_infected_spain_csv(ccaa = 'madrid') # comunidad

    # Balanceamos datos
    temp_provincia, values_infected_provincia, simple_temp_provincia, simple_values_infected_provincia = balance_data(temp_provincia, values_infected_provincia)

    
    model, last_infected_data, last_weather_data = load_and_retrain_model(weather_data = simple_temp_provincia, infected_data = simple_values_infected_provincia, training_window=training_window)

    predictions = sequential_prediction(model=model, initial_value= last_infected_data, heat_initial_value = last_weather_data, training_window=training_window, weather_forecast=forecast_temperature)

    # Cargamos el scaler de infectados y hacemos la transformada inversa de los datos
    infected_scaler = get_infected_scaler()

    predictions = infected_scaler.inverse_transform(predictions)

    # Esto es lo que devuelve el modelo
    print(predictions)

    return 'ok'
    

if __name__ == '__main__':    

    app.run(host="localhost", port=5000,debug=True, threaded=True)
    
