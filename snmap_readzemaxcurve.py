from astropy.table import Table


def readcurve(direc, filelist):
    filesnew = []
    keys = ['ID', 'xangle', 'yangle', 'radii', 'EnergyIn']
    types = [int, float, float, list, list]
    for filen in filelist:
        filesnew.append(direc + '\\' + filen)
    master = Table(names=keys, dtype=types)
    ident = 0
    for filename in filesnew:
        ident += 1
        filer = open(filename)
        datalines = []
        linenumber = 0
        fieldline = ''
        for line in filer:
            linenumber += 1
            if linenumber == 15:
                fieldline = line.strip(' (deg)\n')
            elif linenumber >= 19:
                datalines.append(line.strip('\n'))

        field = fieldline[-14:]
        field = field.split(',')
        xangle = float(field[0])
        yangle = float(field[1])
        locid = int(ident)
        datasplit = []
        for datapoint in datalines:
            datasplit.append(datapoint.split('\t'))
        radiidirt = []
        energiesdirt = []
        for point in datasplit:
            radiidirt.append(point[0])
            energiesdirt.append(point[1])
        radiistr = []
        energiesstr = []
        for entry in radiidirt:
            radiistr.append(entry.replace(' ', ''))
        for entry in energiesdirt:
            energiesstr.append(entry.replace(' ', ''))
        radii = []
        energies = []
        for radius in radiistr:
            radii.append(float(radius))
        for energy in energiesstr:
            energies.append(float(energy))
        toap = [locid, xangle, yangle, radii, energies]
        master.add_row(toap)
    return master
