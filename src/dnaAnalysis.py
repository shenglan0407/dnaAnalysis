import numpy as np
import utilities
from scipy.optimize import curve_fit

def gaussian(x,mean,sigma,amp):
    return amp*np.exp(-(x-mean)**2/2./sigma**2)

def normal(x,mean,sigma):
    return 1./(sigma*np.sqrt(2.*np.pi))*np.exp(-(x-mean)**2/2./sigma**2)

def pull_outliers(data,m):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else 0.
    return data[s<m],data[s>m]

# this should be a debug function
def make_histograms(data,sig_cutoff):

#   separate data by outliers (side) and not outliers (center)
    center,side=pull_outliers(data,sig_cutoff)
    
#   make two histograms
    bin_range=(np.min(side),np.max(side))
    n_center,bins_center=np.histogram(center,bins=150,range=bin_range)
    n_side,bins_side=np.histogram(side,bins=150,range=bin_range)
    
    return bins_center,n_center,bins_side,n_side
    
def train(data, sig_cutoff):
    
    bins_center,n_center,bins_side,n_side = make_histograms(data,sig_cutoff)
    
#   get the x-axis for gaussian fit 
    side_x=bins_side[n_side>0]
    center_x=bins_center[n_center>0]
    
#   gaussian fit to outliers. if fails, returns None
    try:
        coefs_side,_=curve_fit(gaussian,side_x,n_side[n_side>0])
    except RuntimeError:
        utilities.printWarnMsg("One failure in gaussian fit")
        return
        
#   compute residual by interpolating fit to outliers . Fit residuals
    g_left=n_center[n_center>0]-gaussian(center_x,*coefs_side)
    try:
        coefs_center,_=curve_fit(gaussian,center_x,g_left)
    except RuntimeError:
        utilities.printWarnMsg("One failure in gaussian fit")
        return
    
    return np.array([coefs_center,coefs_side])

def reduce():
    return
    
def transfrom():
    return

def predict():
    return
    