import glob
import os


povme_template = '''
LoadInclusionPointsFilename INCL_FILENAME
#LoadSeedPointsFilename      SEED_FILENAME
PDBFileName                 PDB_FILENAME
OutputFilenamePrefix        OUTPUT_PREFIX
NumProcessors 1
'''
#def makeIniText(incl_filename, seed_filename, pdb_filename, output_prefix):
def makeIniText(incl_filename, seed_filename, pdb_filename, output_prefix):
    this_ini = povme_template
    this_ini = this_ini.replace('INCL_FILENAME', incl_filename)
    this_ini = this_ini.replace('SEED_FILENAME', seed_filename)
    this_ini = this_ini.replace('PDB_FILENAME', pdb_filename)
    output_prefix = os.path.join(os.getcwd(),
                                 'secondary_povme_outputs',
                                 prefix,
                                 prefix+'_')
    this_ini = this_ini.replace('OUTPUT_PREFIX', output_prefix)
    return this_ini

primary_inclusions = glob.glob('primary_povme_outputs/*/*_frameInfo/*inclusion.npy')

for primary_inclusion in primary_inclusions:
    basename = os.path.basename(primary_inclusion)
    targ_id = basename.split('_')[0]
    chain_id = basename.split('_')[1]
    lig_resid = basename.split('_')[2]
    cand_id = basename.split('_')[3]
    primary_seed = primary_inclusion.replace('inclusion','seed')
    incl_filename = os.path.abspath(primary_inclusion)
    seed_filename = os.path.abspath(primary_seed)
    pdb_filename = os.path.abspath('hiResApos_clean/hiResApo-%s_%s.pdb' %(targ_id,
                                                                    cand_id))
    prefix = basename.replace('_inclusion.npy','')
    # Here I'm passing in the seed region as the inclusion to be stricter
    ini_text = makeIniText(incl_filename, seed_filename, pdb_filename, prefix)
    with open('secondary_povme_inis/%s.ini'%(prefix), 'wb') as of:
        of.write(ini_text)
    
                                   
    
