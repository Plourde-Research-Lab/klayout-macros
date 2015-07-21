import sys

from cpw_design import cpw

print "{:f} GHz".format(cpw(l=float(sys.argv[1])).f0()*1e-9)