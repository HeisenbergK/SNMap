# SNMap

### Code Necessity and Nunction:

This code is the result of the need to map the S/N ratio for a given astronomical instrument, by utilizing 
it's calculated atmospherically convolved PSF and the intended exposure time.

### Code Inputs:

To work, the code requires the following input data:
- The curves of Ensquared energy fraction (grad) vs. radius from centroid (μm) for the instrument, as produced by Zemax OpticStudio<sup>&reg;</sup> &rarr; files 
- Intended exposure time (s) &rarr; texp
- Minimum sky magnitude (mag<sub>AB</sub>/arcsec<sup>2</sup>) &rarr; msky
- Maximum magnitude of the stars to be observed (mag<sub>AB</sub>) &rarr; mstar
- Total efficiency of the CCD (e<sup>-</sup>/γ). That is the number of electrons produced per incident photon at the band requested &rarr; qccd
- CCD gain (e<sup>-</sup>/ADU) &rarr; gain
- CCD readout noise (e<sup>-</sup>) &rarr; readn
- Pixel width (μm/px) &rarr; aside
- Field-of-view (arcsec) &rarr; fov
- Attenuation per surface (grad). Fraction of incident light, transmitted through the surface &rarr; eta
- Number of total surfaces (grad) &rarr; snum
- Total CCD pixels (px<sup>2<\sup>) &rarr; pixn
- Diameter of the primary mirror of the telescope (cm) &rarr; dtel
- Filter width (Å) &rarr; sigfil
- Filter central wavelength (Å) &rarr; lam
- Intended read level (grad). The fraction of the ensquared energy inside the used aperture &rarr; level
- Extra attenuation (grad) &rarr; exloss 

### Code Methodology: