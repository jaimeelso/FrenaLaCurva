from aemet import Aemet, Estacion
import json


filename = "config.ini"

# Open the file as f.
# The function readlines() reads the file.
texto = ""
file1 = open(filename) 
Lines = file1.readlines()  
# Strips the newline character 
for line in Lines:          
    texto = line.rstrip('\n')
print("imprimiendo..")
print (texto)
aemet = Aemet(texto)
aemet.set_api_key = texto
estaciones = Estacion.get_estaciones()[:3]
datos = []
anyo_inicio, anyo_fin = 2016, 2017 + 1


for estacion in estaciones:
    print('{}: {}'.format(estacion['indicativo'], estacion['nombre']))
    for anyo in range(anyo_inicio, anyo_fin):
        vcm = aemet.get_valores_climatologicos_mensuales(anyo, estacion['indicativo'])
        resultado = {
            'estacion': estacion,
            'valores_climatologicos': vcm,
            'anyo': anyo
        }
        datos.append(resultado)

print(json.dumps(datos, indent=2))