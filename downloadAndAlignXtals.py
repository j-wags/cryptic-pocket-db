import glob
import os
import shutil
hiResApoPdbs = glob.glob('hiResApos/*.pdb')

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


for hiResApoPdb in hiResApoPdbs:
    target_pdb = hiResApoPdb.split('-')[1].split('_')[0]
    candidate_pdb = hiResApoPdb.split('_')[1].split('.')[0]
    candidate_basename = os.path.basename(hiResApoPdb)
    #rot_candidate_file = 'rot-' + candidate_basename
    #if os.path.exists(os.path.join('aligned_candidates', rot_candidate_file)):
    #    continue
    target_filename = target_pdb+'.pdb'
    if not os.path.exists(os.path.join('aligned_targets', target_pdb+'_A.pdb')):
        if not os.path.exists(os.path.join('targets', target_filename)):
            os.system('wget http://www.rcsb.org/pdb/files/%s.pdb.gz' %(target_pdb))
            os.system('gunzip %s.pdb.gz' %(target_pdb))
            shutil.move(target_filename, 'targets')
        target_filename = os.path.join('targets',target_filename)
        # Separate target xtal by chain
        lines = open(target_filename).readlines()
        atom_lines = [i for i in lines if ((i[:4] == 'ATOM') or (i[:6] == 'HETATM'))]
        chains = set([i[21] for i in atom_lines])
        for chain in chains:
            lines_to_write = [i for i in atom_lines if i[21]==chain]
            # Make sure the ligand is in this xtal chain
            lig_id = targ_dict[target_pdb]['lig_id']
            lig_in_chain = False
            for line in lines_to_write:
                if lig_id == line[17:20]:
                    lig_in_chain = True
                    break
            if lig_in_chain == False:
                continue
            output_chain_file = os.path.join('targets_split',
                                             '%s_%s.pdb' %(target_pdb, chain))
            rot_chain_file = 'rot-%s_%s.pdb' %(target_pdb, chain)

            with open(output_chain_file, 'wb') as of:
                of.write('\n'.join(lines_to_write))
            os.system('$SCHRODINGER/utilities/structalign %s %s > align_%s_%s.out' %(hiResApoPdb, output_chain_file, target_pdb, candidate_pdb))
            shutil.move(rot_chain_file, 'aligned_targets')

    # Clean up
    #shutil.move(rot_candidate_file, 'aligned_candidates')
    #os.remove('rot-'+target_filename)
    
    #c += 1 
    #if c==10:
        #1/0
    
