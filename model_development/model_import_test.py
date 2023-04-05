import tensorflow as tf
import pandas as pd
from keras.models import load_model


def pred_reshape(x):
    return x.values.reshape((1, *x.shape))


df = pd.read_csv('../stock_cache.csv')

# model = tf.saved_model.load('../src/model/model_150_v2')
model = load_model('../src/model/model_150_v2')

df = df[df['Symbol'] == 'GOOG'][['Open', 'High', 'Low', 'Close', 'Volume']]

X_test = pred_reshape(df.iloc[-140:-20])
y_test = pred_reshape(df.iloc[-20:]['Close'])

print(X_test.shape, y_test.shape)

model.evaluate(X_test, y_test, batch_size=4, verbose=2)

