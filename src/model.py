import numpy as np
from sklearn.preprocessing import StandardScaler
from weather import *
from data_builder import *
import warnings
with warnings.catch_warnings():  
    warnings.filterwarnings("ignore",category=FutureWarning)
    import tensorflow as tf
    import keras
    from keras.layers import Dense, Input, LSTM, Add, Embedding, Flatten, SimpleRNN
    from keras.layers.core import Dropout
    from keras.layers.merge import concatenate
    from keras.models import Model
    from keras.layers import Concatenate
    from keras.models import Sequential
    from keras import regularizers

DATA_FOLDER =  os.path.dirname(os.getcwd()) + '/data/'
MODEL_FOLDER =  os.path.dirname(os.getcwd()) + '/model/'

def create_model(training_window = 1):

    tf.keras.backend.clear_session()

    # Branch for infected data
    infected_model = Sequential()
    infected_model.add(LSTM(units = 5, input_shape = (training_window,1), activation = 'relu'))
    infected_model.add(Dropout(0.1))
    infected_model.add(Dense(units = 10, activation= 'relu'))


    # Branch for heat data
    heat_model = Sequential()
    heat_model.add(LSTM(units = 8, input_shape = (training_window,1), activation = 'relu'))
    heat_model.add(Dropout(0.1))
    heat_model.add(Dense(units = 10, activation= 'relu'))

    # Merge layer
    merge_layer = concatenate([infected_model.output, heat_model.output])
    hidden = Dense(units=10, activation='relu', activity_regularizer=regularizers.l1(0.001))(merge_layer)
    output = Dense(units=1, activation='linear')(hidden)


    model = Model(inputs=[infected_model.input, heat_model.input], outputs=output)

    return model

def compile_model(model):
    model.compile(loss='mean_absolute_error', optimizer='adam')
    
def train_model(model, X_train, y_train, epochs = 150):
    history = model.fit(x = X_train, y = y_train, epochs = epochs, shuffle = False)
    return history

def evaluate_model(model, X_test, y_test):
    loss = model.evaluate(x = X_test, y = y_test)
    return loss

def predict_model(model, X_test):
    predictions = model.predict(x = X_test)
    return predictions

def sequential_prediction(model, initial_value, heat_initial_value, scaler, training_window, weather_forecast = None):
    weather_forecast = np.array([15.7, 12.5, 14.1, 13.2, 14.6, 14.5, 16.1])

    a = np.reshape(initial_value, (1,training_window))
    b = easy_window(data = weather_forecast, training_window = training_window)
    b = np.reshape(b,(len(b),training_window))
    weather_forecast = np.concatenate([a,b])

    predictions = [pred for pred in initial_value]
    new_predictions = []

    for day in range(len(weather_forecast)):
        prediction_period = np.array([predictions[i] for i in range(training_window)])

        prediction_period = np.reshape(prediction_period, (1,training_window,1))
        weather_period = np.reshape(weather_forecast[day], (1,training_window,1))

        p = model.predict(x = [prediction_period, weather_period])[0]

        new_predictions.append(p)
        predictions.append(p)


    return new_predictions

def easy_window(data, training_window):
    period, new_data = [], []
    i = 0
    for inicio in range(len(data[:-training_window + 1])):
        for i in range(training_window):
            period.append(data[inicio+i])

        new_data.append(period)
        i = 0
        period = []

    return np.array(new_data)

# Esta funcion entrena el modelo con los datos de China y Corea. Ese modelo es guardado para ser entrenado con los datos de la
# comunidad autónoma

def create_and_train_model():
    training_window = 3
    test_size = 0.0

    # Cogemos datos de tiempo
    values_weather, simple_values_weather = read_weather_csv(filename = 'wuhan.csv')
    values_weather_kr, simple_values_weather_kr = read_weather_csv(filename = 'korea.csv')

    # Cogemos datos de infectados
    values_infected, simple_values_infected = read_infected_csv(name='Hubei', country=False)
    values_infected_kr, simple_values_infected_kr = read_infected_csv(name='Korea, South', country=True)

    # Balanceamos datos
    values_weather, values_infected, simple_values_weather, simple_values_infected = balance_data(values_weather, values_infected)
    values_weather_kr, values_infected_kr, simple_values_weather_kr, simple_values_infected_kr = balance_data(values_weather_kr, values_infected_kr)

    # Escalamos datos de infectados
    infected_scaler = StandardScaler()
    infected_scaler.fit(simple_values_infected_kr.reshape(-1,1))
    simple_values_infected = infected_scaler.transform(simple_values_infected.reshape(-1,1))
    simple_values_infected_kr = infected_scaler.transform(simple_values_infected_kr.reshape(-1,1))

    # Escalamos datos de temperature
    weather_scaler = StandardScaler()
    weather_scaler.fit(simple_values_weather_kr.reshape(-1,1))
    simple_values_weather = infected_scaler.transform(simple_values_weather.reshape(-1,1))
    simple_values_weather_kr = infected_scaler.transform(simple_values_weather_kr.reshape(-1,1))

    # Separamos datos tiempo
    X_train_weather, X_test_weather, y_train_weather, y_test_weather = split_data(values= simple_values_weather, test_size = test_size, training_window=training_window)
    X_train_weather_kr, X_test_weather_kr, y_train_weather_kr, y_test_weather_kr = split_data(values= simple_values_weather_kr, test_size = test_size, training_window=training_window)

    # Separamos datos de infectados
    X_train_infected, X_test_infected, y_train_infected, y_test_infected = split_data(values= simple_values_infected, test_size=test_size, training_window=training_window)
    X_train_infected_kr, X_test_infected_kr, y_train_infected_kr, y_test_infected_kr = split_data(values= simple_values_infected_kr, test_size=test_size, training_window=training_window)

    # Creamos modelo
    model = create_model(training_window=training_window)
    print(model.summary())

    # Compilamos modelo
    compile_model(model=model)

    # Entrenamiento
    train_model(model=model, X_train=[X_train_infected_kr, X_train_weather_kr], y_train=y_train_infected_kr, epochs = 100)
    train_model(model=model, X_train=[X_train_infected, X_train_weather], y_train=y_train_infected, epochs = 100)

    # Guardamos modelo
    model_path = MODEL_FOLDER + '/model.h5'
    model.save(model_path)