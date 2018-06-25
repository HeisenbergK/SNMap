from astropy.table import Table
import numpy as np
from scipy import interpolate
from math import ceil
import matplotlib.pyplot as plt


def plotter(tabin, fov, pixn):
    datx = list(tabin['xangle'])        # x coordinates in deg
    daty = list(tabin['yangle'])        # y coordinates in deg
    sns = list(tabin['sigma p'])        # S/N for position
    res = np.sqrt(pixn)                 # resolution in px
    fov /= (60.*60.)                      # field-of-view in deg
    pls = fov/res                       # platescale in deg/px
    datx = np.divide(datx, pls)         # x coordinates in px
    daty = np.divide(daty, pls)         # y coordinates in px
    keys = ['X', 'Y', 'Z']
    dat = [datx, daty, sns]
    reference = Table(names=keys, data=dat)
    reference.pprint(max_width=-1, max_lines=-1)
    xun = []
    yun = []
    for entry in datx:
        if entry not in xun:
            xun.append(entry)
    for entry in daty:
        if entry not in yun:
            yun.append(entry)
    xx, yy = np.meshgrid(xun, yun)
    zz = np.multiply(xx, 0.0)
    for i in range(0, len(yun)):
        for j in range(0, len(xun)):
            res = 0.0
            for k in reference:
                if k['X'] == xun[j] and k['Y'] == yun[i]:
                    res = float(k['Z'])
            zz[i][j] = res
    func = interpolate.interp2d(xx, yy, zz)
    newx = np.linspace(ceil(min(xun)), ceil(max(xun)), num=1000)
    newy = np.linspace(ceil(min(yun)), ceil(max(yun)), num=1000)
    newzz = func(newx, newy)
    newxx, newyy = np.meshgrid(newx, newy)
    plt.pcolormesh(newxx, newyy, newzz, cmap='RdBu')
    plt.title('Systematic Uncertainty in Polarization')
    plt.xlabel('X(px) ref.: O/A')
    plt.ylabel('Y(px) ref.: O/A')
    clb = plt.colorbar()
    clb.ax.set_title(r'$\delta{}_{p}$ $\%{}$')
    plt.show()
    '''
    plt.clf()
    newnewxx = np.add(newxx, -min(newxx))
    newnewyy = np.add(newyy, -min(newyy))
    newnewxx = np.divide(newnewxx, max(newnewxx))
    newnewyy = np.divide(newnewyy, max(newnewyy))
    newnewxx = np.multiply(newnewxx, (60.*fov))
    newnewyy = np.multiply(newnewyy, (60.*fov))
    plt.pcolormesh(newnewxx, newnewyy, newzz, cmap='RdBu')
    plt.title('Systematic Uncertainty in Polarization')
    plt.xlabel('X(px) ref.: O/A')
    plt.ylabel('Y(px) ref.: O/A')
    clb = plt.colorbar()
    clb.ax.set_title(r'$\delta{}_{p}$ $\%{}$')
    plt.show()
    '''
