from flask import Flask,render_template,jsonify
import json

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



if __name__ == '__main__':    

    app.run(host="10.10.200.1", port=5000,debug=True)
    
