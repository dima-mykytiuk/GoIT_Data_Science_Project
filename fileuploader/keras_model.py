import numpy as np
from keras.models import load_model
import tensorflow as tf
from PIL import Image
import keras_cv


def load_image(filename):
    img = tf.keras.utils.load_img(filename, target_size=(32, 32))
    img = tf.keras.utils.img_to_array(img)
    img = img.reshape(32, 32, 3)
    return img


def image_classify(filename, model):
    classes = ["Airplane", "Automobile", "Bird", "Cat", "Deer", "Dog", "Frog", "Horse", "Ship", "Truck"]
    img = load_image(filename)
    model = load_model(model)
    result = model.predict(np.expand_dims(img, axis=0))
    prediction = result[0]
    result = np.argmax(prediction)
    if prediction[result] < 0.85:
        return ["Invalid photo"]
    else:
        return [classes[result], float(str(prediction[result])[:4])]
    