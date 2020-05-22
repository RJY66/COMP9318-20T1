import numpy as np


def logistic_regression(data, labels, weights, num_epochs, learning_rate):  # do not change the heading of the function
    data = np.insert(data, 0, np.ones(data.shape[0]), axis=-1)
    for i in range(0, num_epochs):
        temp = pow((np.exp(np.dot(data, weights) * -1.0) + 1), -1)
        weights += np.dot(labels - temp, data) * learning_rate
    return weights
