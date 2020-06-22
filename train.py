#!/usr/bin/env python3
import os
import chess.pgn
from state import State
import keras
import numpy as np
from keras.utils import Sequence
from keras import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense

class ChessValueDataset(Sequence):
    def __init__(self):
        dat = np.load("processed/dataset.npz", allow_pickle=True)
        self.X = dat["arr_0"]
        self.Y = dat["arr_1"]

    def __len__(self):
        return self.X.shape[0]

    def __getitem__(self, idx):
        return {"X": self.X[idx], "Y": self.Y[idx]}



chess_dataset = ChessValueDataset()

num_classes = 128

model = Sequential()
input_shape = 5, 8, 8
model.add(Conv2D(16, kernel_size=(3, 3), activation="relu", input_shape=input_shape, padding="same"))
model.add(Conv2D(32, kernel_size=(3, 3), activation="relu", padding="same"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation="relu"))
model.add(Dropout(0.3))
model.add(Dense(num_classes, activation="softmax"))
model.compile()

model.summary()

model.fit(x=X, y=y)

model.save("nets/value.pth")

