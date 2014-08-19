#!/usr/bin/env python

from pylab import *
import matplotlib, numpy as np
from geostatsmodels import variograms

def hscattergram( data, pwdist, lag, tol ):
    '''
    Input:  (data)    NumPy array with three columns, the first two 
                      columns should be the x and y coordinates, and 
                      third should be the measurements of the variable
                      of interest
            (lag)     the lagged distance of interest
            (tol)     the allowable tolerance about (lag)
            (pwdist)  a square pairwise distance matrix
    Output:           h-scattergram figure showing the distribution of
                      measurements taken at a certain lag and tolerance
    '''
    # calculate the pairwise distances
    indices = variograms.lagindices( pwdist, lag, tol )
    # collect the head and tail measurements
    head = data[ indices[:,0], 2 ]
    tail = data[ indices[:,1], 2 ]
    # create a scatterplot with equal axes
    fig, ax = subplots()
    ax.scatter( head, tail, marker="o", facecolor="none", edgecolor="k", alpha=0.5 );
    ax.set_aspect("equal");
    # set the labels and the title
    ax.set_ylabel("$z(u+h)$");
    ax.set_xlabel("$z(u)$");
    ax.set_title("Lags Between "+str(lag-tol)+" and "+str(lag+tol))
    # grab the limits of the axes
    xmin, xmax = ax.get_xlim();
    ymin, ymax = ax.get_ylim();
    # calculate the covariance and annotate
    cv = variograms.covariance( data, indices );
    ax.text( xmin*1.25, ymin*1.050, 'Covariance = {:3.2f}'.format(cv) );
    # calculate the semivariance and annotate
    sv = variograms.semivariance( data, indices );
    ax.text( xmin*1.25, ymin*1.025, 'Semivariance = {:3.2f}'.format(sv) );
    show();

def laghistogram( data, pwdist, lags, tol ):
    '''
    Input:  (data)    NumPy array with three columns, the first two 
                      columns should be the x and y coordinates, and 
                      third should be the measurements of the variable
                      of interest
            (pwdist)  the pairwise distances
            (lags)    the lagged distance of interest
            (tol)     the allowable tolerance about (lag)
    Output:           lag histogram figure showing the number of
                      distances at each lag
    '''
    # collect the distances at each lag
    indices = [ variograms.lagindices( pwdist, lag, tol ) for lag in lags ]
    # record the number of indices at each lag
    indices = [ len( i ) for i in indices ]
    # create a bar plot
    fig, ax = subplots()
    ax.bar( lags+tol, indices )
    ax.set_ylabel('Number of Lags')
    ax.set_xlabel('Lag Distance')
    ax.set_title('Lag Histogram')
    show();
    
def svplot( data, lags, tol, model=None ):
    '''
    Input:  (data)    NumPy array with three columns, the first two 
                      columns should be the x and y coordinates, and 
                      third should be the measurements of the variable
                      of interest
            (lags)    the lagged distance of interest
            (tol)     the allowable tolerance about (lag)
            (model)   model function taking a distance and returning
                      an approximation of the semivariance
    Output:           empirical semivariogram
    '''
    h, sv = variograms.semivariogram( data, lags, tol )
    sill = np.var( data[:,2] )
    fig, ax = subplots()
    if model:
        ax.plot( h, model(h), 'r' )
    ax.plot( h, sv, 'ko-' )
    ax.set_ylabel('Semivariance')
    ax.set_xlabel('Lag Distance')
    ax.set_title('Semivariogram')
    ax.text( tol*3, sill*1.025, str( np.round( sill, decimals=3 ) ) )
    ax.axhline( sill, ls='--', color='k' )
    show();

def spaniplot( data, pwdist, lag, tol, angle, atol ):
    '''
    SPatial ANIsotropy PLOT
    '''
    index = variograms.lagindices( pwdist, lag, tol )
    anindex = variograms.anilagindices( data, pwdist, lag, tol, angle, atol )
    
    fig, ax = subplots()

    # plot the lagged distances
    for pair in index:
        head, tail = data[pair]
        hx, hy, hz = head
        tx, ty, tz = tail
        x = [ hx, tx ]
        y = [ hy, ty ]
        ax.plot( x, y, 'k-', lw=2, alpha=0.25 )
        
    # plot the lagged distances within 
    # the anisotropy angle and tolerance
    for pair in anindex:
        head, tail = data[pair]
        hx, hy, hz = head
        tx, ty, tz = tail
        x = [ hx, tx ]
        y = [ hy, ty ]
        ax.plot( x, y, 'r-', lw=1 )
        
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

# this is a colormap that ranges from yellow to purple to black
cdict = {'red':   ((0.0, 1.0, 1.0),
                   (0.5, 225/255., 225/255. ),
                   (0.75, 0.141, 0.141 ),
                   (1.0, 0.0, 0.0)),
         'green': ((0.0, 1.0, 1.0),
                   (0.5, 57/255., 57/255. ),
                   (0.75, 0.0, 0.0 ),
                   (1.0, 0.0, 0.0)),
         'blue':  ((0.0, 0.376, 0.376),
                   (0.5, 198/255., 198/255. ),
                   (0.75, 1.0, 1.0 ),
                   (1.0, 0.0, 0.0)) }
                   
YPcmap = matplotlib.colors.LinearSegmentedColormap('my_colormap',cdict,256)
