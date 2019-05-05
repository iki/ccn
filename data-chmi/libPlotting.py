#!/usr/bin/env python3.6
#-*- coding: utf-8 -*-

# Copyright (C) 2013-2019 T. J.-Y. Derrien
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>


from numpy import genfromtxt, loadtxt, chararray
import glob
import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import matplotlib.cm as cm
from matplotlib import rc
from matplotlib.legend_handler import HandlerLine2D

## Plots a heat-map color picture from a scattered mesh
# @param X: 1D-array
# @param Y: 1D-array
# @param Z: f(X, Y)
# @param QuantityTitle: string with title (LaTeX accepted)
# @param filename:      string with filename (EPS and PNG will be generated)
def plot2dHeatMap(BrutX, BrutY, BrutZ, QuantityTitle, filename, ShowFinalPlot=True): #{{{
  Header="[plot2dHeatMap: ]"
  #print len(BrutX)
  #print len(BrutY)
  #print len(BrutZ)
  X=list(set(BrutX))
  Y=list(BrutY)
  #Z=DensityMax2Dsorted
  YY, XX = np.meshgrid(X, Y)
  # If the size is big enough, let's make a plot.
  #if(len(DensityMax2D) >= 2): #{{{
  if(len(BrutZ) >= 2): #{{{
      ##try:
      triang = tri.Triangulation(BrutX, BrutY)
      triang.set_mask(np.hypot(BrutX[triang.triangles].mean(axis=1),
                               BrutY[triang.triangles].mean(axis=1))
                      < 0.000000015)
      refiner = tri.UniformTriRefiner(triang)
      tri_refi, z_test_refi = refiner.refine_field(BrutZ, subdiv=3)
      #plt.figure()
      #plt.title(r'$N_{exc}(E_1,E_2)$, $\lambda_1=$'+str(wavelength1*1E9)+r'nm, $\lambda_2=$'+str(wavelength2*1E9)+'nm.')
      fig = plt.figure()
      #ax = fig.add_subplot(111) #, projection='3d')
      ##plt.gca().set_aspect('equal')
      plt.title(QuantityTitle)
      ##plt.xlabel(r'$E_1$ (V/nm)')
      ##plt.ylabel(r'$E_2$ (V/nm)')
      ##CS = plt.imshow(XX, YY, DensityMax2Dsorted) #, cmap=plt.cm.Blues)
      ##CS = plt.contourf(XX, YY, DensityMax2Dsorted, cmap=plt.cm.Blues)
      ##CS = ax.plot_wireframe(XX, YY, DensityMax2Dsorted) #, cmap=plt.cm.Blues) #FAILS: WHY do we have ground values ?! 
      ##CS = ax.plot_surface(XX, YY, DensityMax2DsortedShape) #, cmap=plt.cm.Blues) #FAILS: WHY do we have ground values ?! 
      #CS = ax.scatter(BrutX, BrutY, BrutZ) #, cmap=plt.cm.Blues) #WORKS but limited to boring dots
      #CS = ax.plot_trisurf(BrutX, BrutY, BrutZ, cmap=plt.cm.Blues, antialiased=True, edgecolor='none') #WORKS
      ##ax.view_init(90, 90)
      ##See https://matplotlib.org/gallery/images_contours_and_fields/tricontour_smooth_user.html#sphx-glr-gallery-images-contours-and-fields-tricontour-smooth-user-py
      
      plt.triplot(triang, lw=0.1, color='grey')
      levels = np.linspace(np.min(BrutZ), np.max(BrutZ), 10)
      #cmap = cm.get_cmaps(name='terrain', lut=None)
      cmap = cm.get_cmap(name='Blues', lut=None)
      plt.tricontourf(tri_refi, z_test_refi, levels=levels, cmap=cmap)
      #plt.tricontour(tri_refi, z_test_refi, levels=levels,
              ##colors=['0.25', '0.5', '0.5', '0.5', '0.5'],
              ##linewidths=[1.0, 0.5, 0.5, 0.5, 0.5])
      plt.colorbar()
      plt.tight_layout()
        #except:
            #CS = -1
            #print Header+"** Warning: failed to produce one of the plots."
        
      #print np.shape(BrutX), np.shape(BrutY), np.shape(BrutZ)
      #print np.shape(Xi), np.shape(Yi)
      #print np.shape(XXi), np.shape(YYi)
      #print np.shape(BicolorNeFinal)
      
      #CS = ax.scatter(XXi, YYi, BicolorNeFinal) #, cmap=plt.cm.Blues) #WORKS
      
      #CS = ax.plot_trisurf(Xi, Yi, BicolorNeFinal, cmap=plt.cm.Spectral)
      
      #CS = ax.contour(XX, YY, Z, cmap=plt.cm.Blues) #WORKS
      #plt.colorbar(CS)
      
      plt.savefig(filename+'.eps')
      plt.savefig(filename+'.png')
      print(Header, "** Info: saved ", filename, "eps|png.")
      if(ShowFinalPlot==1):
        plt.show()
#}}}
  
def plot2dScatteredPoints(BrutX, BrutY, BrutZ, QuantityTitle, filename, ShowFinalPlot=True): #{{{
  Header="[plot2dScatteredPoints: ]"
  #print len(BrutX)
  #print len(BrutY)
  #print len(BrutZ)
  #X=list(set(BrutX))
  #Y=list(BrutY)
  #Z=DensityMax2Dsorted
  #YY, XX = np.meshgrid(X, Y)
  # If the size is big enough, let's make a plot.
  #if(len(DensityMax2D) >= 2): #{{{
  if(len(BrutZ) >= 2): #{{{
      ##try:
      #triang = tri.Triangulation(BrutX, BrutY)
      #triang.set_mask(np.hypot(BrutX[triang.triangles].mean(axis=1),
                              #BrutY[triang.triangles].mean(axis=1))
                      #< 0.15)
      #refiner = tri.UniformTriRefiner(triang)
      #tri_refi, z_test_refi = refiner.refine_field(BrutZ, subdiv=3)
      #plt.figure()
      #plt.title(r'$N_{exc}(E_1,E_2)$, $\lambda_1=$'+str(wavelength1*1E9)+r'nm, $\lambda_2=$'+str(wavelength2*1E9)+'nm.')
      fig = plt.figure()
      ax = fig.add_subplot(111) #, projection='3d')
      ##plt.gca().set_aspect('equal')
      #plt.title(QuantityTitle)
      ##plt.xlabel(r'$E_1$ (V/nm)')
      ##plt.ylabel(r'$E_2$ (V/nm)')
      ##CS = plt.imshow(XX, YY, DensityMax2Dsorted) #, cmap=plt.cm.Blues)
      ##CS = plt.contourf(XX, YY, DensityMax2Dsorted, cmap=plt.cm.Blues)
      ##CS = ax.plot_wireframe(XX, YY, DensityMax2Dsorted) #, cmap=plt.cm.Blues) #FAILS: WHY do we have ground values ?! 
      ##CS = ax.plot_surface(XX, YY, DensityMax2DsortedShape) #, cmap=plt.cm.Blues) #FAILS: WHY do we have ground values ?! 
      CS = ax.scatter(BrutX, BrutY, 10*BrutZ) #, cmap=plt.cm.Blues) #WORKS but limited to boring dots
      #CS = ax.plot_trisurf(BrutX, BrutY, BrutZ, cmap=plt.cm.Blues, antialiased=True, edgecolor='none') #WORKS
      ##ax.view_init(90, 90)
      ##See https://matplotlib.org/gallery/images_contours_and_fields/tricontour_smooth_user.html#sphx-glr-gallery-images-contours-and-fields-tricontour-smooth-user-py
      
      #plt.triplot(triang, lw=0.1, color='grey')
      #levels = np.linspace(np.min(BrutZ), np.max(BrutZ), 10)
      #cmap = cm.get_cmaps(name='terrain', lut=None)
      #cmap = cm.get_cmap(name='Blues', lut=None)
      #plt.tricontourf(tri_refi, z_test_refi, levels=levels, cmap=cmap)
      #plt.tricontour(tri_refi, z_test_refi, levels=levels,
              ##colors=['0.25', '0.5', '0.5', '0.5', '0.5'],
              ##linewidths=[1.0, 0.5, 0.5, 0.5, 0.5])
      #plt.colorbar()
      plt.tight_layout()
        #except:
            #CS = -1
            #print Header+"** Warning: failed to produce one of the plots."
        
      #print np.shape(BrutX), np.shape(BrutY), np.shape(BrutZ)
      #print np.shape(Xi), np.shape(Yi)
      #print np.shape(XXi), np.shape(YYi)
      #print np.shape(BicolorNeFinal)
      
      #CS = ax.scatter(XXi, YYi, BicolorNeFinal) #, cmap=plt.cm.Blues) #WORKS
      
      #CS = ax.plot_trisurf(Xi, Yi, BicolorNeFinal, cmap=plt.cm.Spectral)
      
      #CS = ax.contour(XX, YY, Z, cmap=plt.cm.Blues) #WORKS
      #plt.colorbar(CS)
      
      #plt.savefig(filename+'.eps')
      plt.savefig(filename+'.png')
      print(Header, "** Info: saved ", filename, "png.")
      if(ShowFinalPlot==1):
        plt.show()
#}}}
