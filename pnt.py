#! /usr/bin/env python

import re, pickle, gzip, math
import numpy as np

class LinearFloatIntInterpolator:
    def __init__(self, amin, astep):
        self.amin = amin
        self.astep = astep
    def float_to_int(self, a):
        return int(round((a - self.amin) / self.astep))
    def int_to_float(self, i):
        return self.amin + i*self.astep

class PntFile:
    def __init__(self, filename=None):
        self.npoints = 469758
        self.a = np.zeros((self.npoints,3))
        if filename is not None:
            self.filename = filename
            i = 0
            with open(filename, "r") as f:
                for line in [line.strip() for line in f.readlines()]:
                    y,x,t = [float(s) for s in re.split(r'\s+', line)]
                    self.a[i,0] = x
                    self.a[i,1] = y
                    self.a[i,2] = t
                    i = i + 1
    def write(self,filename):
        with open(filename, "w") as f:
            for i in range(0,len(self.a)):
                f.write("%8.4f %9.4f  %7.2f\n" % (self.a[i,1], self.a[i,0], self.a[i,2]))
    @staticmethod
    def avg(pfiles):
        presult = PntFile()
        nfiles = len(pfiles)
        for i in range(0,presult.npoints):
            presult.a[i,0] = pfiles[0].a[i,0] # x
            presult.a[i,1] = pfiles[0].a[i,1] # y
            presult.a[i,2] = sum( [ p.a[i,2] for p in pfiles ] ) / nfiles
        return presult
    @staticmethod
    def subtract(pfile_a,pfile_b):
        presult = PntFile()
        for i in range(0,presult.npoints):
            presult.a[i,0] = pfile_a.a[i,0] # x
            presult.a[i,1] = pfile_a.a[i,1] # y
            presult.a[i,2] = pfile_a.a[i,2] - pfile_b.a[i,2]
        return presult

class PntGrid:
    def __init__(self):
        self.width    = 1385 # width nX
        self.height   = 596  # height nY
        self.gridsize = 1/24.0
        self.minX     = -124.6875
        self.minY     = 24.5625
        self.xTr      = LinearFloatIntInterpolator(self.minX, self.gridsize)
        self.yTr      = LinearFloatIntInterpolator(self.minY, self.gridsize)
    @staticmethod
    def load_pkzfile(pkzfile):
        with gzip.open(pkzfile, "rb") as f:
            return pickle.load(f)
    def load_pntfile(self,pntfile):
        self.a = np.empty((self.height,self.width))
        self.a.fill(np.nan)
        used = {}
        n = 0
        for p in pntfile.a:
            i = self.yTr.float_to_int(p[1])
            j = self.xTr.float_to_int(p[0])
            k = "%1d,%1d" % (i,j)
            if k in used:
                print "warning: duplication for k=%s" % k
            else:
                used[k] = True
            try:
                self.a[i,j] = p[2]
            except IndexError:
                print "index out of range for k=%s" % k
        return self
    @staticmethod
    def avg(gs):
        """Compute and return the average of a list of grid files gs."""
        g = PntGrid()
        g.a = np.empty((g.height,g.width))
        g.a.fill(np.nan)
        ba = gs[0].a
        for i in range(0,g.height):
            for j in range(0,g.width):
                if not math.isnan(ba[i,j]):
                    sum = 0
                    for k in range(0,len(gs)):
                        sum += gs[k].a[i,j]
                    g.a[i,j] = sum / len(gs)
        return g
    @staticmethod
    def subtract(g1, g2):
        """Compute and return the difference of two grid file, g1 - g2."""
        g = PntGrid()
        g.a = np.empty((g.height,g.width))
        g.a.fill(np.nan)
        for i in range(0,g.height):
            for j in range(0,g.width):
                if not math.isnan(g1.a[i,j]):
                    g.a[i,j] = g1.a[i,j] - g2.a[i,j]
        return g
    @staticmethod
    def divide(g1, g2, factor=1.0):
        """Compute and return the quotient of two grid file, g1 / g2, optionally
        also multiplying by a scalar factor."""
        g = PntGrid()
        g.a = np.empty((g.height,g.width))
        g.a.fill(np.nan)
        for i in range(0,g.height):
            for j in range(0,g.width):
                if (not math.isnan(g1.a[i,j])
                    and not math.isnan(g2.a[i,j])
                    and not g2.a[i,j] == 0):
                    g.a[i,j] = factor * g1.a[i,j] / g2.a[i,j]
        return g
