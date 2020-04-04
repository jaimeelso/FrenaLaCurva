import numpy as np
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

def create_model():

    tf.keras.backend.clear_session()

    # Branch for infected data
    infected_model = Sequential()
    model.add(LSTM(units = 30, input_shape = (1,1), activation = 'relu'))
    model.add(Dense(units = 30, activation= 'relu'))

    # Branch for heat data
    heat_model = Sequential()
    model.add(LSTM(units = 30, input_shape = (1,1), activation = 'relu'))
    model.add(Dense(units = 30, activation= 'relu'))

    # Merge layer
    merge_layer = concatenate([infected_model.output, heat_model.output])
    hidden = Dense(units=(3*dense_units), activation='relu')(merge_layer)
    output = Dense(units=output_size, activation='linear')(hidden)
    model.add(Dense(units = 1, activation='linear'))

    model = Model(inputs=[infected_model.input, heat_model.input], outputs=output)

    return model

def compile_model(model):
    model.compile(loss='mean_absolute_error', optimizer='adam')
    
def train_model(model, X_train, y_train):
    history = model.fit(x = X_train, y = y_train, validation_split = 0.2, epochs = 200, shuffle = False)
    return history

def evaluate_model(model, X_test, y_test):
    loss = model.evaluate(x = X_test, y = y_test)
    return loss

def sequential_prediction(model, initial_value, days):
    
    initial_value = np.array(initial_value).reshape(1,1,1)
    predictions = [initial_value]
    i = 0

    for day in range(days):
        predictor = predictions[i].reshape(1,1,1)
        predictions.append(model.predict(x = predictor)[0])
        i += 1

    print(predictions)
    return predictions