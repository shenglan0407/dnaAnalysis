import numpy as np
import utilities
import sys
from scipy.optimize import curve_fit

def gaussian(x,mean,sigma,amp):
    return amp*np.exp(-(x-mean)**2/2./sigma**2)

def normal(x,mean,sigma):
    return 1./(np.abs(sigma)*np.sqrt(2.*np.pi))*np.exp(-(x-mean)**2/2./sigma**2)

def pull_outliers(data,m):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else 0.
    return data[s<m],data[s>m]

# this should be a debug function
def make_histograms(data,sig_cutoff,num_bins):

#   separate data by outliers (side) and not outliers (center)
    center,side=pull_outliers(data,sig_cutoff)
    
#   make two histograms
    bin_range=(np.min(side),np.max(side))
    n_center,bins_center=np.histogram(center,bins=num_bins,range=bin_range)
    n_side,bins_side=np.histogram(side,bins=num_bins,range=bin_range)
    
    return bins_center,n_center,bins_side,n_side
    
def train(data, sig_cutoff,num_bins):
    
    bins_center,n_center,bins_side,n_side = make_histograms(data,sig_cutoff,num_bins)
    
#   get the x-axis for gaussian fit 
    side_x=bins_side[:-1][n_side>0]
    center_x=bins_center[:-1][n_center>0]
    
#   gaussian fit to outliers. if fails, returns None
    try:
        coefs_side,_=curve_fit(gaussian,side_x,n_side[n_side>0])
    except RuntimeError:
        utilities.printWarningMsg("One failure in gaussian fit")
        return np.zeros((2,3))
        
#   compute residual by interpolating fit to outliers . Fit residuals
    g_left=n_center[n_center>0]-gaussian(center_x,*coefs_side)
    try:
        coefs_center,_=curve_fit(gaussian,center_x,g_left)
    except RuntimeError:
        utilities.printWarningMsg("One failure in gaussian fit")
        return np.zeros((2,3))
    
    return np.array([coefs_center,coefs_side])

def predict(data,model):
    try:
        assert data.shape[0] == model.shape[0] 
    except AssertionError:
        utilities.printErrorMsg("Model and data shape mismatch")
        return 0., 0. 
    
    p_c = []
    p_u = []
    
    for i in range(data.shape[0]):
        if (model[i][0][1]==0):
            n_c=0
        else:
            n_c = normal(data[i],model[i][0][0],model[i][0][1])
            
        if(model[i][1][1]==0):
            n_u = 0
        else:
            n_u = normal(data[i],model[i][1][0],model[i][1][1])
        if(n_c==0 and n_u==0):
            p_c.append(0.)
            p_u.append(0.)
        else:
            p_c.append(n_c/(n_c+n_u))
            p_u.append(n_u/(n_c+n_u))
    
    p_c=np.array(p_c)
    p_u=np.array(p_u)
    
    return p_c,p_u

    
def transform(data,pr_c,pr_u):
    av_pc=np.mean(pr_c,axis=1)
    av_pu=np.mean(pr_u,axis=1)
    
    weights=np.array([av_pc[i]/av_pu[i] for i in range(av_pc.shape[0])])
#     weights=weights/np.sum(weights)
    
    weighted_average=np.zeros(data[0].shape)
    for i in range(len(weights)):
        weighted_average += data[i]*weights[i]
    return weighted_average, weights

def predict_transform(all_data, model,psi_skip=10):
    try:
        assert all_data.shape[1]-psi_skip == model.shape[0] 
    except AssertionError:
        utilities.printErrorMsg("Model and data shape mismatch")
        return 0., 0. 
    
    pr_u=[]
    pr_c=[]
    for i in range(all_data.shape[0]):
        prs=predict(all_data[i][psi_skip:],model)
        pr_u.append(prs[1])
        pr_c.append(prs[0])
    
    pr_c=np.array(pr_c)
    pr_u=np.array(pr_u)
    
    weighted_average,weights = transform(all_data,pr_c,pr_u)
    
    return weighted_average,weights

def cospsi(delta, q, wavelen):
    theta = np.arcsin(wavelen * q / (4*np.pi))
    return np.cos(delta)*np.cos(theta)**2 + np.sin(theta)**2
    



    
