from snmap_readzemaxcurve import *
import numpy as np
import matplotlib.pyplot as plt
from math import ceil
from snmap_plotter import *

keys = ['ID', 'xangle', 'yangle', 'R', 'A', 'S', 'B', 'T', 'N', 'S/N', 'sigma p']
types = [int, float, float, float, float, float, float, float, float, float, float]
units = ['grad', 'deg', 'deg', 'um', 'px', 'ADU', 'ADU', 'ADU', 'ADU', 'grad', '%']
mastertable = Table(names=keys, dtype=types)
for i in range(0, len(keys)):
    mastertable[keys[i]].unit = units[i]

c = 2.99792458*np.power(10.0, 18.0)                                      # speed of light in angstroem/s
h = 6.62607004*np.power(10.0, -27.0)                                     # planck constant in erg/Hz

folder = 'C:\\Users\\johny\\Dropbox\\Ensquared_Energy_profiles\\3_inch'  # folder containing the ensquared energy curves
files = ['f1.txt', 'f2.txt', 'f3.txt', 'f4.txt', 'f5.txt',
         'f6.txt', 'f7.txt', 'f8.txt', 'f9.txt']                         # filenames of the curve files
texp = 20.0*60.0                                                         # exposure time in seconds
msky = 18.0                                                              # sky magnitude in AB/arcsec^2
mstar = 16.5                                                             # stars to be observed magnitude in AB
qccd = 0.80                                                              # CCD efficiency in e-/photon
gain = 2.8                                                               # CCD gain in e-/ADU
readn = 1.8                                                              # CCD readout noise in e-
aside = 15.0                                                             # pixel width in um/px
fov = 35.0*60.0                                                          # field-of-view in arcseconds
eta = 0.98                                                               # attenuation per surface norm 1 in grad
snum = 34                                                                # number of surfaces in grad
pixn = np.power(4*1024, 2)                                               # total number of pixels in px
dtel = 100.0                                                             # telescope diameter in cm
sigfil = 1065.6                                                          # filter width in Angstroem
lam = 6349                                                               # effective filter wavelength in Angstroems
level = 0.9999                                                           # required source level in grad
exloss = 0.8                                                             # attenuation in grad

read = readcurve(direc=folder, filelist=files)

nu = c/lam                                                               # effective filter wavelength in Hz
sigfil = c/sigfil                                                        # filter width in Hz
fsky = 3631.0 * np.power(10.0, -23.0) * np.power(10.0, (-msky/2.5))      # sky flux in erg/s/cm^2/Hz/arcsec^2
fstar = 3631.0 * np.power(10.0, -23.0) * np.power(10.0, (-mstar/2.5))    # star flux in erg/s/cm^2/Hz
fB = fsky * np.pi * 0.25 * np.power(dtel, 2.0) * sigfil * texp * (qccd/(gain*h*nu)) *\
     np.power(fov, 2.0) * np.power(eta, snum) *\
     np.power(pixn, -1.0) * np.power(4.0, -1.0) * exloss                 # background luminosity in ADU/px
fS = fstar * np.pi * 0.25 * np.power(dtel, 2.0) * sigfil * texp * (qccd/(gain*h*nu)) *\
     np.power(eta, snum) * np.power(4.0, -1.0) * exloss                  # star total energy in ADU
source = level * fS                                                      # source counts in ADU

for i in range(0, len(files)):
    row = read[i]
    curid = row['ID']
    xangle = row['xangle']
    yangle = row['yangle']
    radii = row['radii']
    energies = row['EnergyIn']
    newradii = np.linspace(min(radii), max(radii), num=1000)
    newenergies = np.interp(newradii, radii, energies)
    redenergies = np.subtract(newenergies, level)
    # print(len(radii), len(energies), len(newradii), len(newenergies), len(redenergies))
    redenergiesfit = np.polyfit(newradii, redenergies, deg=15)
    poly = np.poly1d(redenergiesfit)
    '''
    plt.clf()
    plt.plot(newradii, redenergies, 'r', newradii, poly(newradii), 'b')
    plt.show()
    '''
    roots = np.roots(redenergiesfit)
    roots = roots[np.isreal(roots)]
    roots = np.real(roots)
    roots = roots[roots > 0.0]
    root = min(roots)
    s = source
    pixin = ceil(np.pi * np.power(root, 2.0) * np.power(aside, -2.0))
    b = pixin * fB
    t = s + b
    n = np.sqrt(t+b+((2*readn*pixin)/gain))
    snr = s/n
    sigmap = np.power(2.0*snr, -1.0)
    sigmap *= 100
    toap = [curid, xangle, yangle, root, pixin, s, b, t, n, snr, sigmap]
    mastertable.add_row(toap)

mastertable.write('test.ecsv', format='ascii.ecsv', overwrite=True)
mastertable.pprint(max_lines=-1, max_width=-1)
plotter(mastertable, fov, pixn)
