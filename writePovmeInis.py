import glob
import os

hiResApoPdbs = glob.glob('hiResApos_clean/*.pdb')

povme_template = '''
DefinePocketByLigand   LIGAND_RESNAME
PDBFileName                 PDB_FILENAME
OutputFilenamePrefix          OUTPUT_PREFIX
NumProcessors 1 
'''

def makeIniText(ligand_resname, pdb_filename, prefix):
    this_ini = povme_template
    this_ini = this_ini.replace('LIGAND_RESNAME', ligand_resname)
    abs_pdb_filename = os.path.join(os.path.abspath(pdb_filename))
    this_ini = this_ini.replace('PDB_FILENAME', abs_pdb_filename)
    out_prefix = os.path.join(os.getcwd(), 'primary_povme_outputs', prefix, prefix+'_')
    this_ini = this_ini.replace('OUTPUT_PREFIX', out_prefix)
    return this_ini
    
# Make target info dictionary
targ_dict = {}
for cand in hiResApoPdbs:
    cand_id = os.path.basename(cand).split('_')[1].split('.')[0]
    targ_id = os.path.basename(cand).split('-')[1].split('_')[0]
    targ_dict[targ_id] = {}
    targ_dict[targ_id]['candidate_id'] = cand_id
    targ_dict[targ_id]['candidate_file'] = os.path.abspath(cand)
    #targ_dict[targ_id]['target_file'] = os.path.abspath(os.path.join('targets', targ_id + '.pdb'))
    targ_info_txt = os.path.join('infoDicts', targ_id+'.txt')
    targ_dict[targ_id]['info_txt'] = os.path.abspath(targ_info_txt)
    targ_lig_id = [i.split()[1] for i in open(targ_info_txt).readlines() if 'ligand' in i][0]
    targ_dict[targ_id]['lig_id'] = targ_lig_id

    # Prepare POVME config files for each xtal chain
    targ_chain_files = glob.glob('aligned_targets/rot-%s_?.pdb' %(targ_id))
    for targ_chain_file in targ_chain_files:
        chain = targ_chain_file.split('_')[-1].replace('.pdb','')
        prefix = '_'.join([targ_id, chain, targ_lig_id, cand_id])
        ini_text = makeIniText(targ_lig_id, targ_chain_file, prefix)
        with open('primary_povme_inis/%s.ini' %(prefix),'wb') as of:
            of.write(ini_text)
        
        
        
    
    
