import os
import numpy as np

sigma = 42.5   # resolution
mu = 697       # elastic channel number
x = np.arange(1000)
norm_counts = 1/(sigma * np.sqrt(2.0*np.pi)) * np.exp(- (x - mu)**2 / (2 * sigma**2))


def fake_tof(fname):
    outfname = os.path.join('FakeTOF', os.path.basename(fname))
    outf = open(outfname, 'w')
    with open(fname, 'r') as f:
        for line in f:
            if line.startswith('#'):
                if '#  TOF channels' in line:
                    line = '#  TOF channels                 1000'
                if '#  Time per channel' in line:
                    line = '#  Time per channel           1.3 microsecs'
                if '#  Delay time' in line:
                    line = '#  Delay time              0.0 microsecs'
                if '# 64    1' in line:
                    line = '# 64    1000'
                print(line.strip('\n'), file=outf)
    data = np.loadtxt(fname)
    for i in range(64):
        row = "{0} ".format(i) + np.array2string(data[i,1]*norm_counts, precision=0, separator=' ',
                suppress_small=True, max_line_width=10000).strip('[').strip(']')
        print(row, file=outf)

    outf.close()


if __name__ == '__main__':
    name_template = 'FakeTOF/orig/nmt{}.d_dat'
    runs = range(1, 801)
    for i in runs:
        filename = name_template.format(format(i, '0>3'))
        fake_tof(filename)
