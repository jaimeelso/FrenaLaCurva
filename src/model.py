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


def create_model():

    tf.keras.backend.clear_session()

    # Branch for infected data
    infected_model = Sequential()
    infected_model.add(LSTM(units = 5, input_shape = (1,1), activation = 'tanh'))
    #infected_model.add(Dropout(0.1))
    infected_model.add(Dense(units = 10, activation= 'tanh'))


    # Branch for heat data
    heat_model = Sequential()
    heat_model.add(LSTM(units = 5, input_shape = (1,1), activation = 'tanh'))
    #heat_model.add(Dropout(0.1))
    heat_model.add(Dense(units = 10, activation= 'tanh'))

    # Merge layer
    merge_layer = concatenate([infected_model.output, heat_model.output])
    hidden = Dense(units=10, activation='relu', activity_regularizer=regularizers.l1(0.001))(merge_layer)
    output = Dense(units=1, activation='linear')(hidden)


    model = Model(inputs=[infected_model.input, heat_model.input], outputs=output)

    return model

def compile_model(model):
    model.compile(loss='mean_absolute_error', optimizer='adam')
    
def train_model(model, X_train, y_train):
    history = model.fit(x = X_train, y = y_train, epochs = 150, shuffle = False)
    return history

def evaluate_model(model, X_test, y_test):
    loss = model.evaluate(x = X_test, y = y_test)
    return loss

def predict_model(model, X_test):
    predictions = model.predict(x = X_test)
    return predictions

def sequential_prediction(model, initial_value, days, scaler, weather_forecast = None):
    initial_value = np.array(initial_value).reshape(1,1,1)
    predictions = [initial_value]
    heat = np.array([15.7, 12.5, 14.1, 13.2, 14.6, 14.5, 16.1])
    #heat = np.random.randint(30, size=days)
    heat = scaler.transform(heat.reshape(-1,1))
    i = 0
    for day in range(days):
        predictor = predictions[i].reshape(1,1,1)
        predictions.append(model.predict(x = [predictor, heat[day].reshape(1,1,1)])[0])
        i += 1


    return predictions