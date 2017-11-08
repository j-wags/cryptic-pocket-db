
import __main__
import sys
import glob
#__main__.pymol_argv = [ 'pymol', '-cq'] #put -cq here to suppress pymol output
__main__.pymol_argv = [ 'pymol', '-q'] #put -cq here to suppress pymol output

import pymol
pymol.finish_launching()

if len(sys.argv) != 3:
    print "python", sys.argv[0], "target_pdb apo_pdb"

target_id = sys.argv[1].lower()
apo_id = sys.argv[2].lower()

apo_prefix = 'hiResApo-%s_%s' %(target_id, apo_id)
apo_name = '%s.pdb' %(apo_prefix)
apo_file = 'hiResApos_clean/%s' %(apo_name)

target_files = glob.glob('aligned_targets/rot-%s_?.pdb')

print apo_file
pymol.cmd.load(apo_file)

pymol.util.cba(13,apo_prefix)
for target_file in target_files:
    pymol.cmd.load(target_file)
    target_name = target_file.split('/')[-1].replace('.pdb','')
    print target_name
    pymol.util.cba(15,target_name)

'''    
pdbCode = sys.argv[1].strip('.').strip('/')
if len(pdbCode) != 4:
    1/0

predFiles = glob.glob('./%s/*' %(pdbCode))
predFiles.sort()
for predFile in predFiles:
    pymol.cmd.load(predFile)
pymol.cmd.fetch(pdbCode)

pymol.util.mass_align(pdbCode,0)
pymol.preset.publication("all")
pymol.cmd.symexp("sym", pdbCode, '(%s)' %(pdbCode), 8)
pymol.util.cba(11,pdbCode)
'''
