import numpy as np

def sigmoid(m, a = 1.0):
    """
    1 / (1 + exp(-a * m))
    """
    return 1 / (1 + np.exp(-a * m))

def d_sigmoid(m, a = 1.0):
    raise NotImplementedError()

def identity(m):
    """
    f: m -> m
    """
    return m

def d_identity(m):
    raise NotImplementedError()

def tanh(m, a = 1.0):
    """
    ( exp(a * m) - exp(-a * m) ) / ( exp(a * m) + exp(-a * m) )
    """
    return np.tanh(a * m)

def d_tanh(m, a = 1.0):
    raise NotImplementedError()

def softmax(m):
    """
    exp(m_i) / sum_i( exp(m_i) ), i is index of dimension
    """
    s = np.exp(m)
    return s / np.sum(s)

def d_softmax(m):
    raise NotImplementedError()