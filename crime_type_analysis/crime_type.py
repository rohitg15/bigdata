import sys
import numpy as np

from sklearn.metrics import accuracy_score
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD, RMSprop
from keras.layers.normalization import BatchNormalization
from keras.callbacks import EarlyStopping


def get_crime_type(x_train_file, y_train_file, x_test_file, y_test_file, op_file, algo_type):
    X_trainset = np.genfromtxt(x_train_file, delimiter=',')
    Y_trainset = np.genfromtxt(y_train_file, delimiter=',')
    X_testset = np.genfromtxt(x_test_file, delimiter=',')
    Y_testset = np.genfromtxt(y_test_file, delimiter=',')
    crimes = ["THEFT", "BATTERY", "DECEPTION", "NARCOTICS", "BURGLARY"]

    #print "XTRAIN : ",X_trainset.shape
    #print "YTRAIN : ",Y_trainset.shape
    #print "XTEST : ",X_testset.shape
    #print "YTEST : ",Y_testset.shape

    #exit(0)
    # train a keras Sequential model
    model = Sequential()
    model.add(Dense(256, input_shape=(434,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))

    model.add(Dense(256))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))

    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))

    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))

    model.add(Dense(5))
    model.add(Activation('softmax'))
    # do SGD or rms asap
    if algo_type == 0:
        sgd = SGD(lr=0.01, decay=0, momentum=0.1, nesterov=False)
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=["accuracy"])
        model.fit(X_trainset, Y_trainset, batch_size=32, nb_epoch=5, verbose=1,
              validation_data=(X_testset, Y_testset), validation_split=0.2,
          callbacks=[EarlyStopping(monitor='val_loss', patience=2)])
    else:
        model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
        model.fit(X_trainset, Y_trainset, batch_size=32, nb_epoch=5, verbose=1,
              validation_data=(X_testset, Y_testset), validation_split=0.2,
          callbacks=[EarlyStopping(monitor='val_loss', patience=2)])


    print('Classifcation rate : %02.4f ' % model.evaluate(X_testset, Y_testset)[1])
    # obtain class results and corresponding probabilities
    op = []
    model_class = model.predict_classes(X_testset, batch_size=32)
    size = len(model_class)
    probabilities = model.predict_proba(X_testset, batch_size=32)
    for i in xrange(size):
        # get max probability
        max_val = -1
        col_size = len(probabilities[i])
        for j in xrange(col_size):
            if max_val < probabilities[i][j]:
                max_val = probabilities[i][j]
        # store output array
        op.append(str(crimes[model_class[i]]) + "," + str(max_val))
    # write to file
    with open(op_file, "w") as file:
        file.write("\n".join(op))




if __name__ == "__main__":
    argc = len(sys.argv)
    if argc != 7:
        print "usage: %s x_train_file y_train_file x_test_file y_test_file op_file sgd/rms1(0/1)" % (sys.argv[0])
        exit(0)
    get_crime_type(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], int(sys.argv[6]))
