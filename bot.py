import numpy as np
import keras
from keras.models import Sequential
from keras.models import Model
from keras.models import load_model
from keras.layers import Dense
from keras.optimizers import Adam
# Init your variables here

# Put your bot name here
name = "Langue"
ia = Sequential()


# Bender strategy : return the first element in the available cells.
# That always generates horizontal line in the top of the board 

class net(object):
    def __init__(self, reseauExistant):
        if not reseauExistant:     # On regarde si le reseau de nerones existe deja ou si il faut le creer
            self.opt = Adam(lr=0.1, beta_1=0.9, beta_2=0.999)
            self.model = Sequential()
        else:
            self.model = load_model("reseauLangue.H5")

    def training(self, train_Data, target_data):
        self.model.add(Dense(49, input_dim=49, activation='relu'))
        self.model.add(Dense(48 * 7, activation='relu'))
        self.model.add(Dense(48 * 47 * 4, activation='relu'))
        self.model.add(Dense(48 * 47 * 2, activation='relu'))
        self.model.add(Dense(48 * 47, activation='relu'))
        self.model.add(Dense(24 * 47, activation='relu'))
        self.model.add(Dense(12 * 47, activation='relu'))
        self.model.add(Dense(6 * 47, activation='relu'))
        self.model.add(Dense(3 * 47, activation='relu'))
        self.model.add(Dense(47, activation='relu'))
        self.model.add(Dense(1, activation='relu'))
        self.model.compile(optimizer=self.opt, loss='mean_squared_error')
        self.model.fit(train_Data,target_data, epochs=1000, verbose=1)

    def save(self):
        self.model.save("reseauLangue.H5")

    def predict(self, board):
        return self.model.predict(board, verbose=2)


def findBestChoice(prediction, available_cells):
    print(prediction)


def play(board, available_cells, player):
    reseau = Sequential(True)
    prediction = reseau.predict(board)
    return available_cells[0]
