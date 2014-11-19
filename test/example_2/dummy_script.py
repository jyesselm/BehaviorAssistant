#!/usr/bin/python
from __future__ import print_function
import matplotlib
matplotlib.use('Agg')
from matplotlib.pylab import *
import sys

scale = int(sys.argv[1])

figure(1)
clf()
r = arange(0,10,0.5)
if scale == 1:
    plot(r, scale*r, c='blue')
else:
    plot(r, scale*r, c='red')
savefig('dummy_plot.png')


print('This is an stdout message: Argument is %s' % scale)

print('This is an stderr message: Argument is %s' % scale, file=sys.stderr)
