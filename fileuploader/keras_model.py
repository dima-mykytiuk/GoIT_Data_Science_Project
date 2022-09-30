import numpy as np
from keras.models import load_model
import tensorflow as tf
from PIL import Image


def load_image(filename):
    f = Image.open(filename)
    array = tf.keras.preprocessing.image.img_to_array(f)
    resized_img_array = tf.image.resize(array, (32, 32))
    return resized_img_array


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
        return [classes[result], f'{str(prediction[result])[:4]} accuracy']
    