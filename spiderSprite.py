#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# --------------------------------------------------------------> this py file is the main interface of spiderSprite <---------------------------------------------------------------- #
import sys
import os
wd = os.path.abspath(__file__)
wd = os.path.dirname(wd)
help = f'''
Usage: python3 {__file__} subcommand options

subcommand:
    web_ncbi:   Grab 'Non-coding RNA profiling by high throughput sequencing' 'SRA Run Select' record from NCBI.
    biosample:  Generate a file containing all of the biosample, one record per line.
    web_ena:    Grab biosample json download link file from ENA
    download:   Download ncRNA-Seq or miRNA-Seq data with aria2c according filereport_read_run_PRJNAXXXXX_json.txt link

type spiderSprite.py subcommad -h for more subcommad detail
'''
version = '''
v0.1: 2022.11.29
'''

parament = ' '.join(sys.argv[2:])
if len(sys.argv) == 1:
    print(help)
    sys.exit()

if sys.argv[1] == 'web_ncbi':
    cmd = 'python3 ' + wd + '/bin/web_ncbi.py ' + parament
    print(f'EXCUTED CMD: {cmd}')
    os.system(cmd)
elif sys.argv[1] == 'biosample':
    cmd = 'bash ' + wd + '/bin/biosample.sh ' + parament
    print(f'EXCUTED CMD: {cmd}')
    os.system(cmd)
elif sys.argv[1] == 'web_ena':
    cmd = 'python3 ' + wd + '/bin/web_ena.py ' + parament
    print(f'EXCUTED CMD: {cmd}')
    os.system(cmd)
elif sys.argv[1] == 'download':
    cmd = 'python3 ' + wd + '/bin/parse_json.py ' + parament
    print(f'EXCUTED CMD: {cmd}')
    os.system(cmd)
elif sys.argv[1] == '-v':
    print(version)
    sys.exit()
elif sys.argv[1] == '-h':
    print(help)
    sys.exit()
