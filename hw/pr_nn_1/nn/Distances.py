import numpy as np


def xeuclidian(t, y):
    """
    Half of squered Euclidian distance
    :param t: target values
    :param y: predicted values
    """
    return np.sum((t - y) ** 2, axis=1) / 2

def d_xeuclidian(t, y):
    """
    Partial derivative by each of dimensions of the half of squered Euclidian distance
    :param t: target values
    :param y: predicted values
    """
    raise NotImplementedError()

@np.vectorize
def log_Bernoulli_likelihood_elements(t, y):
    return(0 if t == 0 or y == 1 else (t * np.log(y) if y != 0 else t * np.log(np.finfo(float).eps))) + \
          (0 if t == 1 or y == 0 else ((1 - t) * np.log(1 - y) if y != 1 else (1 - t) * np.log(np.finfo(float).eps)))


def log_Bernoulli_likelihood(t, y):
    """
    -sum( t * log(y) + (1 - t) * log(1 - y) )
    :param t: target values
    :param y: predicted values
    """
    return -np.sum(log_Bernoulli_likelihood_elements(t, y), axis=1)

@np.vectorize
def d_log_Bernoulli_likelihood(t, y):
    raise NotImplementedError()


@np.vectorize
def cross_entropy_elements(t, y):
    return t * (np.log(np.finfo(float).eps) if y == 0 else np.log(y))

def cross_entropy(t, y):
    """
    -sum( t * log(y) )
    :param t: target values
    :param y: predicted values
    """
    return -np.sum(cross_entropy_elements(t, y), axis=1)

def d_cross_entropy(t, y):
    raise NotImplementedError()

def euclidian(t, y):
    return np.sqrt(np.sum((t - y) ** 2, axis=1))

def hamming(t, y):
    return np.sum(np.abs(t - y), axis=1)