from astropy.table import Table
master = Table.read('test.ecsv', format='ascii.ecsv')
master.pprint(max_lines=-1, max_width=-1)