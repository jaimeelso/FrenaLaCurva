import numpy as np
import warnings
from sklearn.preprocessing import StandardScaler
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
