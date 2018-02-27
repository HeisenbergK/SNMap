from astropy.table import Table
import numpy as np


def plotter(tabin, fov, pixn):
    datx = list(tabin['xangle'])        # x coordinates in deg
    daty = list(tabin['yangle'])        # y coordinates in deg
    sns = list(tabin['sigma p'])        # S/N for position
    res = np.sqrt(pixn)                 # resolution in px
    fov /= (60*60)                      # field-of-view in deg
    pls = fov/res                       # platescale in deg/px
    datx = np.divide(datx, pls)         # x coordinates in px
    daty = np.divide(daty, pls)         # y coordinates in px
    keys = ['X', 'Y', 'Z']
    dat = [datx, daty, sns]
    reference = Table(names=keys, data=dat)
    reference.pprint(max_width=-1, max_lines=-1)
