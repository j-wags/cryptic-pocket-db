import glob
hiResApos = glob.glob('hiResApos/*pdb')

for hiResApo in hiResApos:
    data = open(hiResApo).readlines()
    data = [line for line in data if line[:6] != 'HETATM']
    cleanFile = hiResApo.replace('hiResApos/','hiResApos_clean/')
    print hiResApo, cleanFile
    with open(cleanFile,'wb') as of:
        of.write(''.join(data))
