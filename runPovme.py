import glob
import os

inis = glob.glob('primary_povme_inis/*ini')

for ini in inis:
    data = open(ini).readlines()
    output_prefix_full = [i.split()[1] for i in data if 'OutputFilenamePrefix' in i][0]
    output_prefix = os.path.basename(output_prefix_full)
    output_folder = '/'+'/'.join(output_prefix_full.split('/')[:-1])

    #if len(glob.glob(output_prefix_full+'*')) == 0:
    if not(os.path.exists(output_folder)):
        os.system('mkdir -p %s' %(output_folder))
        cmd = 'POVME3.py %s &> primary_povme_out_txts/povme_%s.out' %(ini, output_prefix)
        print 'RUNNING:', cmd
        os.system(cmd)
