"""
by Ohad Omrad
"""
"""
this file contain a class with a static method
this method declared the model layers
"""
from keras.models import Sequential
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dropout
from keras.layers.core import Dense
from keras import backend as K

class MyModel:
    @staticmethod
    def build(width, height, depth, classes, finalAct="softmax"):
        """
        Get: 1 -> the imaged dims
             2 -> the categories
             3 -> the final activation function - by defual "softmax"
        """
        """
        initialize the model along with the input shape to be
		"channels last" and the channels dimension itself
        """
        model = Sequential()
        inputShape = (height, width, depth)
        chanDim = -1

		# if we are using "channels first", update the input shape
		# and channels dimension
        if K.image_data_format() == "channels_first":
            inputShape = (depth, height, width)
            chanDim = 1

		# CONV => RELU => POOL
        model.add(Conv2D(32, (3, 3), padding="same", input_shape=inputShape))
        model.add(Activation("sigmoid"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(MaxPooling2D(pool_size=(3, 3)))
        model.add(Dropout(0.25))

		# (CONV => RELU) * 2 => POOL
        model.add(Conv2D(64, (3, 3), padding="same"))
        model.add(Activation("sigmoid"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(Conv2D(64, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

		# (CONV => RELU) * 2 => POOL
        model.add(Conv2D(128, (3, 3), padding="same"))
        
        #model.add(Dropout(0.25))

        model.add(Activation("sigmoid"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(Conv2D(128, (3, 3), padding="same"))
        model.add(Activation("sigmoid"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

		# first (and only) set of FC => RELU layers
        model.add(Flatten())
        model.add(Dense(1024))
        model.add(Activation("sigmoid"))
        model.add(BatchNormalization())
        model.add(Dropout(0.5))

		# softmax classifier
        model.add(Dense(classes))
        model.add(Activation(finalAct))

		# return the constructed network architecture
        return model