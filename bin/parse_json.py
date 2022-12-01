#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys
'''
@File    :   parse_json.py
@Time    :   2022/10/26 15:31:46
@Author  :   zrf 
@Version :   0.0
@Contact :   zrfeng1@gmail.com
@License :   (C)Copyright 2022-, NJAU-CBI
@Desc    :   None
'''
help = '''
this script is designed to download data from ena
    option:
        -i: <dir> --  the directory where the filereprot file is stored
        -o: <dir> --  outputdir, the directory where downloaded file is stored
'''
version = '''
    v0.1
'''
for i in range(1, len(sys.argv)):
    if sys.argv[i] == '-i':
        datadir = sys.argv[i + 1]
    elif sys.argv[i] == '-o':
        outdatadir = sys.argv[i + 1]
    elif sys.argv[i] == '-v':
        print(version)
        sys.exit()
    elif sys.argv[i] == '-h':
        print(help)
        sys.exit()

import pandas as pd
import numpy as np
import os
import time

tmpfile='.' + time.strftime("%Y%m%d%H%M%S", time.localtime())
os.chdir(datadir)
cmd = 'ls filereport* > ' + tmpfile
os.system(cmd)


def detect_downloaded(pattern: str, wd: str):
    df = pd.Series(os.listdir(wd), dtype=str)
    downloaded_libraries = df[df.str.contains(pattern)]
    return downloaded_libraries

def combineJson(file_list):
    """combine all json data

    Arguments:
        file_list {file} -- file contain all json file name\n

    Returns:
        2D dataStructure -- pd.Dataframe
    """
    combine_df = pd.DataFrame()
    for file in np.nditer(file_list):
        print(f'reading {str(file)}')
        tmp_df = pd.read_json(str(file))
        combine_df = pd.concat([combine_df, tmp_df], join='outer')
    return combine_df


cmd = '[ -e ' + outdatadir + ' ] || mkdir ' + outdatadir 
os.system(cmd)

file_list = np.loadtxt(tmpfile, dtype=str)
jsondata = combineJson(file_list)
subset = [
    'run_accession', 'library_layout', 'library_strategy', 'library_selection',
    'fastq_ftp'
]
subjson = jsondata.loc[:, subset]
select_bool = (jsondata.library_strategy == 'ncRNA-Seq') | (jsondata.library_strategy == 'miRNA-Seq')
targetjson = subjson.loc[select_bool]
downloaded = detect_downloaded("SRR\d*.*fastq\.gz", outdatadir).str.split('.').tolist()
list = []
for i in downloaded:
    list.append(i[0])
list = pd.Series(list, dtype=str)
pool = targetjson.run_accession
downloaded_bool = (~pool.isin(list))
ftps = targetjson.fastq_ftp[downloaded_bool]


for i in ftps:
    cmd = f'aria2c -x 16 -s 16 -c -d {outdatadir} ftp://{i}'
    print('start download data with aria2c')
    os.system(cmd)

cmd = 'rm ' + tmpfile
os.system(cmd)

# for i in asperas:
#     cmd = f'ascp -k 1 -QT -l 500m -P 33001 -i /home/riceUsers/fzr/anaconda3/envs/py36/etc/asperaweb_id_dsa.openssh era-fasp@{i} {outdatadir}'
#     print('start download data with aspera...')
#     os.system(cmd)