import os
import sys

runnames=['run296314_NiUxvV_corr.hdf5',
'run296315_9EKBZP_corr.hdf5',
'run296316_ESFLBI_corr.hdf5',
'run296317_bft9pB_corr.hdf5',
'run296318_U0HdUm_corr.hdf5',
'run296319_CryCft_corr.hdf5',
'run296320_yxMKfc_corr.hdf5',
'run296321_OPEq9Z_corr.hdf5',
'run296322_Pza_Fc_corr.hdf5',
'run296323_qKVcyH_corr.hdf5',
'run296324_WQKDUu_corr.hdf5',
'run296325_DAlRWU_corr.hdf5',
'run296326_s80g3G_corr.hdf5',
'run296327_hAq3sJ_corr.hdf5',
'run296328_K_lN4x_corr.hdf5',
'run296329_gen_pO_corr.hdf5',
'run296330_hZXeXz_corr.hdf5',
'run296331_3IUEcN_corr.hdf5',
'run296332_5Hlo3u_corr.hdf5',
'run296333_eBlI3L_corr.hdf5',
'run296334_L6GyQ1_corr.hdf5',
'run296335_DCL24R_corr.hdf5',
'run296336_AHv0WH_corr.hdf5',
'run296337_knl1u6_corr.hdf5',
'run296338_VQ5dYS_corr.hdf5',
'run296339_cZLLwO_corr.hdf5',
'run296340_xli943_corr.hdf5',
'run296341_2t9MZv_corr.hdf5',
'run296342_ij1vhK_corr.hdf5',
'run296343_4IpqnB_corr.hdf5',
'run296344_jCvPEv_corr.hdf5',
'run296345_mH8b6d_corr.hdf5',
'run296346_0qKzYQ_corr.hdf5',
'run296347_qcymKK_corr.hdf5',
'run296348_fIVjxZ_corr.hdf5',
'run296349_x44KLo_corr.hdf5',
'run296350_TBFQ5g_corr.hdf5',
'run296351_SUOEFT_corr.hdf5',
'run296352_GYNwyy_corr.hdf5',
'run296353_kpKuli_corr.hdf5']

data_file = '/data/work/schengu/cxs/dna/sacla_201504/loki/q0.88_qdel5_phipix/'
fileDir = os.path.dirname(os.path.realpath('__file__'))


for this_run in runnames:
    config_file = '%s.cfg'%this_run.split('.')[0]
    with open(os.path.join(fileDir, '../config/fc_ldna088/%s'%config_file),'w') as config:
        config.write('[Data]\n')
        config.write('train_set=%s%s\n'%(data_file,this_run))
        
        config.write('[Outliers]\n')
        config.write('num_bins=300\n')
        config.write('outlier_cutoff=3\n')
        config.write('psi_skip = 10\n')

with open(os.path.join(fileDir, '../scripts/train_fc_ldna088.sh'),'w') as script:
    for this_run in runnames:
        config_file = '%s.cfg'%this_run.split('.')[0]
        script.write("./train.py -i fc_ldna088/%s -o fc_ldna088/%s\n"%(config_file,this_run))
        
