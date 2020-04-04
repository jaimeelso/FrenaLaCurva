from data_builder import *
from model import *
from weather import *
import matplotlib.pyplot as plt

fname = 'wuhan.csv'
test_size = 0.2

# Leemos datos de tiempo
values_weather, simple_values_weather = read_weather_csv(filename = fname)
values_weather_spain, simple_values_weather_spain = temperature_data(name = 'Madrid')

# Leemos datos de infectados
values_infected, simple_values_infected = read_infected_csv(name='Hubei', country=False)
values_infected_spain, simple_values_infected_spain = read_infected_csv(name='Spain', country=True)

# Balanceamos datos
values_weather, values_infected, simple_values_weather, simple_values_infected = balance_data(values_weather, values_infected)
values_weather_spain, values_infected_spain, simple_values_weather_spain, simple_values_infected_spain = balance_data(values_weather_spain, values_infected_spain)

# Separamos datos
X_train_weather, X_test_weather, y_train_weather, y_test_weather = split_data(values= simple_values_weather, test_size = test_size)
X_train_infected, X_test_infected, y_train_infected, y_test_infected = split_data(values= simple_values_infected, test_size=test_size)

X_train_infected_spain, _ , y_train_infected_spain, _ = split_data(values= simple_values_infected_spain, test_size=0.1)
X_train_weather_spain, _ , y_train_weather_spain, _ = split_data(values= simple_values_weather_spain, test_size=0.1)

model = create_model()
print(model.summary())

compile_model(model=model)

"""plt.plot(simple_values_infected)
plt.show()"""

train_model(model=model, X_train=[X_train_infected, X_train_weather], y_train=y_train_infected)
predictions = predict_model(model=model, X_test=[X_train_infected_spain, X_train_weather_spain])
loss = evaluate_model(model=model, X_test=[X_train_infected_spain, X_train_weather_spain], y_test=y_train_infected_spain)
print(loss)


plt.plot(X_train_infected_spain[:,0,0], 'o')
plt.plot(predictions)
plt.show()