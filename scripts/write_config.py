import os
import sys

runnames=['run296314_2Yu2Px_corr.hdf5',
'run296315_JWP6eG_corr.hdf5',
'run296316_B89e_a_corr.hdf5',
'run296317_RxC5pX_corr.hdf5',
'run296318_axwhhW_corr.hdf5',
'run296319_5euwaF_corr.hdf5',
'run296320_QUfA_L_corr.hdf5',
'run296321_W9_4G1_corr.hdf5',
'run296322_WHt6Gx_corr.hdf5',
'run296323_x40p73_corr.hdf5',
'run296324_9MkbaY_corr.hdf5',
'run296325_Fbd1wt_corr.hdf5',
'run296326_ab9r04_corr.hdf5',
'run296327_KeXLYb_corr.hdf5',
'run296328_sNs2zl_corr.hdf5',
'run296329_DNQngL_corr.hdf5',
'run296330_cIhMjJ_corr.hdf5',
'run296331_JGai1s_corr.hdf5',
'run296332_shPojx_corr.hdf5',
'run296333_fEIb72_corr.hdf5',
'run296334_WoodQN_corr.hdf5',
'run296335_wSBDrx_corr.hdf5',
'run296336_G2ozqr_corr.hdf5',
'run296337_998uC2_corr.hdf5',
'run296338_AJTE0n_corr.hdf5',
'run296339_8ECZCR_corr.hdf5',
'run296340_p5RFG6_corr.hdf5',
'run296341_Gj6PIG_corr.hdf5',
'run296342_I3fFZb_corr.hdf5',
'run296343_MTYzLy_corr.hdf5',
'run296344_JlmOgO_corr.hdf5',
'run296345_0S2rxk_corr.hdf5',
'run296346_kdoGwB_corr.hdf5',
'run296347_InuUPy_corr.hdf5',
'run296348_vLZsBm_corr.hdf5',
'run296349_ECoxdk_corr.hdf5',
'run296350_okU_MF_corr.hdf5',
'run296351_rYZZWS_corr.hdf5',
'run296352_MOYjiO_corr.hdf5',
'run296353_uf9KCF_corr.hdf5'
]


data_file = '/data/work/schengu/cxs/dna/sacla_201504/loki/q1.85_qdel5_phipix/'
fileDir = os.path.dirname(os.path.realpath('__file__'))


for this_run in runnames:
    config_file = '%s.cfg'%this_run.split('.')[0]
    with open(os.path.join(fileDir, '../config/fc_ldna185/%s'%config_file),'w') as config:
        config.write('[Data]\n')
        config.write('train_set=%s%s\n'%(data_file,this_run))
        
        config.write('[Outliers]\n')
        config.write('num_bins=300\n')
        config.write('outlier_cutoff=3\n')
        config.write('psi_skip = 10\n')

with open(os.path.join(fileDir, '../scripts/train_fc_ldna185.sh'),'w') as script:
    for this_run in runnames:
        config_file = '%s.cfg'%this_run.split('.')[0]
        script.write("Epython train.py -i fc_ldna185/%s -o fc_ldna185/%s -v\n"%(config_file,this_run))
        
