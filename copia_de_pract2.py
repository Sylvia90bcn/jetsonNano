# -*- coding: utf-8 -*-
"""Copia de Pract2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mYB2XrOJRNAI2kHFrAYO5VXxzgIcrpOh
"""

# Import tensorflow and print current version
import tensorflow as tf
print(tf.__version__)

# Import rest of libraries used in the code. Usually this is done at the beginning of the document but it can be done at any position
import numpy as np
import matplotlib.pyplot as plt
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.optimizers import SGD, Adagrad, Adadelta
from keras.utils import np_utils
from keras.callbacks import LearningRateScheduler
import os

# Hyperparameters:
# They must be carefully select depending on the dataset and model

NB_EPOCH =  30      # Number of training epochs
VALIDATION_SPLIT=0.2 # Size of the validation split taken from the training set. If your dataset has validation split, skip this part.

"""Cargamos el dataset:"""

from google.colab import drive
drive.mount("/content/gdrive")

PATH_OF_DATA= '/content/gdrive/MyDrive/casa'

train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    '/content/gdrive/MyDrive/casa', labels='inferred', subset="training", validation_split=VALIDATION_SPLIT, seed=0)
val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    '/content/gdrive/MyDrive/casa', labels='inferred', subset="validation", validation_split=VALIDATION_SPLIT, seed=0)

train_ds

"""Vamos a visualizar una de las muestras y la clase a la que pertenece:"""

import matplotlib.pyplot as plt
sample = list(train_ds.as_numpy_iterator())[0]    # Tupla con el batch
image = sample[0]                                 # Batch de imagenes
label = sample[1]                                 # Batch de labels
plt.imshow(np.squeeze(image[0])/255.0)
print(label[0])

def process(image,label):
    image = tf.cast(image/255. ,tf.float32)
    image = tf.image.resize(image,(256,256))
    return image,label

train_ds = train_ds.map(process)
val_ds = val_ds.map(process)

# Create a pretrained model.
model = tf.keras.applications.MobileNet(
  include_top=False, weights='imagenet', input_shape=(256,256,3), classes=8)

# Freeze weights
for l in model.layers:
  l.trainable=False;

# Add new classification layer
flat = tf.keras.layers.Flatten()(model.output)
out = tf.keras.layers.Dense(8, activation='softmax')(flat)

model = tf.keras.models.Model(inputs=model.inputs, outputs=out)

model.summary()

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(train_ds, epochs=NB_EPOCH, validation_data=val_ds)

model.evaluate(val_ds)

# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# Save model
OUT_MODEL_PATH= '/content/gdrive/MyDrive/Curso-Jetson/models'
model.save(os.path.join(OUT_MODEL_PATH, 'model-final-pract2.hdf5'))
model.save(os.path.join(OUT_MODEL_PATH, 'model-final-pract2'))

!ls $OUT_MODEL_PATH

