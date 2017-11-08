import glob
import numpy as np
import matplotlib.pyplot as plt
import os

# Full data run
attempted_inis = glob.glob('primary_povme_inis/*ini')
primary_vols = glob.glob('primary_povme_outputs/*/*volumes.tabbed.txt')
secondary_vols = glob.glob('secondary_povme_outputs/*/*volumes.tabbed.txt')
# Small data run
#primary_vols = glob.glob('primary_povme_outputs/5ifl*/*volumes.tabbed.txt')
#secondary_vols = glob.glob('secondary_povme_outputs/5ifl*/*volumes.tabbed.txt')

attempted_ids = [i.split('/')[-1].replace('.ini','') for i in attempted_inis]
primary_ids = [i.split('/')[-1].replace('_volumes.tabbed.txt','') for i in primary_vols]
secondary_ids = [i.split('/')[-1].replace('_volumes.tabbed.txt','') for i in secondary_vols]
sec_ids_set = set(secondary_ids)
both_ids = [i for i in primary_ids if i in sec_ids_set]
both_ids.sort()

#print both_ids
print 'len(attempted_ids)', len(attempted_ids)
print 'len(primary_ids)', len(primary_ids)
print 'len(secondary_ids)', len(secondary_ids)
print 'len(both_ids)', len(both_ids)

ratios = []
pymol_script = []
min_threshold = 0.00
max_threshold = 0.60
id2volsAndRatio = {}
for att_id in attempted_ids:
    primary_file = 'primary_povme_outputs/%s/%s_volumes.tabbed.txt'%(att_id,
                                                                     att_id)
    secondary_file = 'secondary_povme_outputs/%s/%s_volumes.tabbed.txt'%(att_id,
                                                                         att_id)
    if os.path.exists(primary_file):
        primary_vol = np.genfromtxt(primary_file)[1]
    else:
        id2volsAndRatio[att_id] = (None, None, None)
        continue
    if os.path.exists(secondary_file):
        secondary_vol = np.genfromtxt(secondary_file)[1]
    else:
        id2volsAndRatio[att_id] = (primary_vol, None, None)        
        continue
    # If we got this far, both primary and secondary POVMEs were successful
    b_id = att_id
    ratio = secondary_vol/primary_vol
    ratios.append(ratio)
    id2volsAndRatio[b_id] = (primary_vol, secondary_vol, ratio)
    if (ratio > min_threshold) and (ratio < max_threshold):
        pdb_and_chain = '_'.join(b_id.split('_')[:2])
        pdb_id = b_id.split('_')[0]
        if pdb_id[:2] == '5p':
            continue
        hiResApo_file = glob.glob('hiResApos/hiResApo-%s*.pdb' %(pdb_id))[0]
        pymol_script.append('load aligned_targets/rot-%s.pdb' %(pdb_and_chain))
        pymol_script.append('load %s' %(hiResApo_file))
        hiResApo_obj = hiResApo_file.split('/')[-1].replace('.pdb','')
        pymol_script.append('preset.pub_solv("%s")' %(hiResApo_obj))
        aligned_xtal_obj = 'rot-%s' %(pdb_and_chain)
        pymol_script.append('preset.pub_solv("%s")' %(aligned_xtal_obj))
        pymol_script.append('cmd.show("mesh", "%s")' %(hiResApo_obj))
        pymol_script.append('util.cba(33, "%s")' %(aligned_xtal_obj))
        pymol_script.append('util.cba(154, "%s")' %(hiResApo_obj))
        
#with open('under_%s.pml' %(str(show_threshold)),'wb') as of:
with open('between_%s_and_%s.pml' %(str(min_threshold), str(max_threshold)),'wb') as of:
    of.write('\n'.join(pymol_script))

plot = False
if plot:
    plt.hist(ratios, bins=np.arange(0., 1.5, 0.03))
    plt.ylabel('Number of structures')
    plt.xlabel('Apo/Holo pocket volume ratio')
    plt.show()

def getApoChain(holo_id, apo_id):
    data = open('hiResApos/hiResApo-%s_%s.pdb'%(holo_id, apo_id)).readlines()
    chainSet = set()
    for line in data:
        if not('ATOM' == line[:4]):
            continue
        chain = line[21]
        chainSet.add(chain)
    if len(list(chainSet)) > 1:
        print 'error: multiple chains detected in', holo_id, apo_id, chainSet
    return list(chainSet)[0]
    

with open('ratios.csv','wb') as of:
    of.write('holo_id,holo_chain,ligand_resname,apo_id,apo_chain,holo_volume,apo_volume,ratio\n')
    all_keys = id2volsAndRatio.keys()
    all_keys.sort()
    for pair_id in all_keys:
        # b_id example: 4zfi_A_4NJ_2axi
        holo_id, holo_chain, ligand_resname, apo_id = pair_id.split('_')
        primary_vol, secondary_vol, ratio = id2volsAndRatio[pair_id]
        apo_chain = getApoChain(holo_id, apo_id)
        of.write('%s,%s,%s,%s,%s,%s,%s,%s\n'%(holo_id,
                                              holo_chain,
                                              ligand_resname,
                                              apo_id,
                                              apo_chain,
                                              str(primary_vol),
                                              str(secondary_vol),
                                              str(ratio)))
