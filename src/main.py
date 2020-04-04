from data_builder import *
from model import *
from weather import *
import matplotlib.pyplot as plt
import configparser
from sklearn.preprocessing import StandardScaler


test_size = 0.0
spain_pob = float(config['poblation']['spain'])
hubei_pob = float(config['poblation']['hubei'])
korea_pob = float(config['poblation']['korea'])

# Leemos datos de tiempo
values_weather, simple_values_weather = read_weather_csv(filename = 'wuhan.csv')
values_weather_kr, simple_values_weather_kr = read_weather_csv(filename = 'korea.csv')
values_weather_spain, simple_values_weather_spain = temperature_data(name = 'Madrid')

# Leemos datos de infectados
values_infected, simple_values_infected = read_infected_csv(name='Hubei', country=False)
values_infected_kr, simple_values_infected_kr = read_infected_csv(name='Korea, South', country=True)
values_infected_spain, simple_values_infected_spain = read_infected_csv(name='Spain', country=True)

# Balanceamos datos
values_weather, values_infected, simple_values_weather, simple_values_infected = balance_data(values_weather, values_infected)
values_weather_kr, values_infected_kr, simple_values_weather_kr, simple_values_infected_kr = balance_data(values_weather_kr, values_infected_kr)
values_weather_spain, values_infected_spain, simple_values_weather_spain, simple_values_infected_spain = balance_data(values_weather_spain, values_infected_spain)

# Escalamos datos de infectados
infected_scaler = StandardScaler()
infected_scaler.fit(simple_values_infected_spain.reshape(-1,1))
simple_values_infected = infected_scaler.transform(simple_values_infected.reshape(-1,1))
simple_values_infected_kr = infected_scaler.transform(simple_values_infected_kr.reshape(-1,1))
simple_values_infected_spain = infected_scaler.transform(simple_values_infected_spain.reshape(-1,1))

# Escalamos datos de temperature
weather_scaler = StandardScaler()
weather_scaler.fit(simple_values_weather_spain.reshape(-1,1))
simple_values_weather = infected_scaler.transform(simple_values_weather.reshape(-1,1))
simple_values_weather_kr = infected_scaler.transform(simple_values_weather_kr.reshape(-1,1))
simple_values_weather_spain = infected_scaler.transform(simple_values_weather_spain.reshape(-1,1))

# Separamos datos tiempo
X_train_weather, X_test_weather, y_train_weather, y_test_weather = split_data(values= simple_values_weather, test_size = test_size)
X_train_weather_kr, X_test_weather_kr, y_train_weather_kr, y_test_weather_kr = split_data(values= simple_values_weather_kr, test_size = test_size)

# Separamos datos de infectados
X_train_infected, X_test_infected, y_train_infected, y_test_infected = split_data(values= simple_values_infected, test_size=test_size)
X_train_infected_kr, X_test_infected_kr, y_train_infected_kr, y_test_infected_kr = split_data(values= simple_values_infected_kr, test_size=test_size)

X_train_infected_spain, _ , y_train_infected_spain, _ = split_data(values= simple_values_infected_spain, test_size=test_size)
X_train_weather_spain, _ , y_train_weather_spain, _ = split_data(values= simple_values_weather_spain, test_size=test_size)

model = create_model()
print(model.summary())

compile_model(model=model)


# Entrenamiento
train_model(model=model, X_train=[X_train_infected_kr, X_train_weather_kr], y_train=y_train_infected_kr)
train_model(model=model, X_train=[X_train_infected, X_train_weather], y_train=y_train_infected)
train_model(model=model, X_train=[X_train_infected_spain, X_train_weather_spain], y_train=y_train_infected_spain)

predictions = predict_model(model=model, X_test=[X_train_infected_spain, X_train_weather_spain])

new_predictions = sequential_prediction(model=model, initial_value= y_train_infected_spain[-1], days = 7, scaler = weather_scaler)
new_predictions = np.concatenate([predictions, new_predictions], axis = None)

plt.plot(X_train_infected[:,0,0], label = 'China')
plt.plot(X_train_infected_kr[:,0,0], label = 'Korea')
plt.plot(new_predictions, '+', label = 'Spain Prediction')
plt.plot(X_train_infected_spain[:,0,0], '.', label = 'Spain')
plt.title('CoVid-19 Infected')
plt.legend()
plt.show()