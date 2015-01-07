import numpy as np

def l1(m):
    return np.sum(np.abs(m.reshape((1, np.prod(m.shape)))))

def d_l1(m):
    raise NotImplementedError()

def l2(m):
    return 0.5 * np.sum(m.reshape((1, np.prod(m.shape))) ** 2)

def d_l2(m):
    raise NotImplementedError()

def elasticnet(m):
    return l1(m) + l2(m)

def d_elasticnet(m):
    raise NotImplementedError()