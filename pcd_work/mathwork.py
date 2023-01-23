# phx_center: [ 139.79060364  -54.9095192  1004.68945312]
# rs_center: [ 21.37802728 -56.06262758 468.00002456]

import math
import numpy as np

if __name__=='__main__':
    transfer= np.array([[1.54753269e-01,  7.75188953e-01, - 6.12509552e-01,  4.76210299e+02],
     [-9.60020415e-01,  2.64373045e-01,  9.20349774e-02, - 6.02640177e+01],
    [2.33265914e-01, 5.73779748e-01, 7.85108607e-01, 6.60822712e+02],
    [0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]])
    center = np.array([[ 21.37802728, -56.06262758, 468.00002456, 1]]).T
    phx_center = np.dot(transfer, center)
    print(phx_center)

