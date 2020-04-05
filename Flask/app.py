from flask import Flask, render_template, url_for, request, redirect, jsonify, config
import json
import requests

from flask_bootstrap import Bootstrap
app = Flask(__name__)

Bootstrap(app)

@app.route('/',methods=['GET', 'POST'])
def index():    
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
    print("la localizacion es la siguiente "+str(localizacion))
    api_key = "13322246a8ad4613a0ca2608f8942168"
    base_url = 'https://api.weatherbit.io/v2.0/forecast/daily'
    lat = localizacion['latitud']
    lon = localizacion['longitud']

    params = {            
        'lat':lat,
        'lon':lon,
        'days':'7',
        'lang':'es',
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
        
    print(tempArray)

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
        provincia = dataprovince['address_components'][3]['long_name']
        break

    print (provincia)
    return 'ok'
    

    


if __name__ == '__main__':    

    app.run(host="10.10.200.1", port=5000,debug=True)
    
