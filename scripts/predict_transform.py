import numpy as np
import h5py

import matplotlib.pyplot as plt

import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.realpath('__file__')), '../src'))


import dnaAnalysis as da
import time


m185=['run296314_2Yu2Px_corr.hdf5',
'run296315_JWP6eG_corr.hdf5',
'run296316_B89e_a_corr.hdf5',
'run296317_RxC5pX_corr.hdf5',
'run296318_axwhhW_corr.hdf5',
'run296319_5euwaF_corr.hdf5',
'run296320_QUfA_L_corr.hdf5',
'run296321_W9_4G1_corr.hdf5',
'run296322_WHt6Gx_corr.hdf5',
'run296323_x40p73_corr.hdf5']

m088=['run296314_NiUxvV_corr.hdf5',
'run296315_9EKBZP_corr.hdf5',
'run296316_ESFLBI_corr.hdf5',
'run296317_bft9pB_corr.hdf5',
'run296318_U0HdUm_corr.hdf5',
'run296319_CryCft_corr.hdf5',
'run296320_yxMKfc_corr.hdf5',
'run296321_OPEq9Z_corr.hdf5',
'run296322_Pza_Fc_corr.hdf5',
'run296323_qKVcyH_corr.hdf5']

model_path = '/home/qiaoshen/dnaAnalysis/models'
model185_path=['%s/fc_ldna185/%s'%(model_path,i) for i in m185]
model088_path=['%s/fc_ldna088/%s'%(model_path,i) for i in m088]
models088=[h5py.File(this_path,'r') for this_path in model088_path]
models185=[h5py.File(this_path,'r') for this_path in model185_path]

data_path = '/data/work/schengu/cxs/dna/sacla_201504/loki'
data185_path=['%s/q1.85_qdel5_phipix/%s'%(data_path,i) for i in m185]
data088_path=['%s/q0.88_qdel5_phipix/%s'%(data_path,i) for i in m088]
data185=[h5py.File(this_path,'r') for this_path in data185_path]
data088=[h5py.File(this_path,'r') for this_path in data088_path]

skip_psi = 10
# 
# weiAve185=[]
# wei185=[]
# for idx in range(len(m185)):
#     tic=time.clock()
#     dif_cors = data185[idx]['dif_cors'][:]
#     model=models185[idx]['dists'][:]
#     
#     wa,ws=da.predict_transform(dif_cors,model,psi_skip=skip_psi)
#     output=h5py.File('/home/qiaoshen/dnaAnalysis/weighted_ave/fc_ldna185/%s'%m185[idx],'w')
#     output.create_dataset('weighted_average',data=wa)
#     output.create_dataset('weights',data=ws)
#     output.close()
#     weiAve185.append(wa)
#     wei185.extend(ws)
#     toc=time.clock()
#     print("time to tranform %s is %g"%(m185[idx],(toc-tic)))
# # 
# wei185=np.array(wei185)
# Ave185=np.sum(np.array(weiAve185),axis=0)/np.sum(wei185)
# output=h5py.File('/home/qiaoshen/dnaAnalysis/weighted_ave/fc_ldna185/all_runs.hdf5','w')
# output.create_dataset('weighted_average',data=Ave185)
# output.create_dataset('weights',data=wei185)

# plt.figure()
# plt.plot(np.mean(weiAve185,axis=0))
# plt.show()
# 
# plt.figure()
# plt.plot(wei185[1])
# plt.show()

# 
weiAve088=[]
wei088=[]
for idx in range(len(m088)):
    tic=time.clock()
    dif_cors = data088[idx]['dif_cors'][:]
    model=models088[idx]['dists'][:]
    
    wa,ws=da.predict_transform(dif_cors,model,psi_skip=skip_psi)
    print wa.shape
    print ws.shape
    output=h5py.File('/home/qiaoshen/dnaAnalysis/weighted_ave/fc_ldna088/%s'%m088[idx],'w')
    output.create_dataset('weighted_average',data=wa)
    output.create_dataset('weights',data=ws)
    weiAve088.append(wa)
    wei088.extend(ws)
    output.close()
    
    toc=time.clock()
    print("time to tranform %s is %g"%(m185[idx],(toc-tic)))

wei088=np.array(wei088)
Ave088=np.sum(np.array(weiAve088),axis=0)/np.sum(wei088)
output=h5py.File('/home/qiaoshen/dnaAnalysis/weighted_ave/fc_ldna088/all_runs.hdf5','w')
output.create_dataset('weighted_average',data=Ave088)
output.create_dataset('weights',data=wei088)
output.close()