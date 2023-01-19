from diffnets.data_processing import ProcessTraj, WhitenTraj

pTraj = ProcessTraj(['trajs/WT/','trajs/H172Y/'],['WT.pdb','H172Y.pdb'],'processedTrajs/',atom_sel='(not resname NME and not resname D7I) and (name CA or name CB or name C or name N)')
pTraj.run()
wTraj = WhitenTraj('processedTrajs/')
wTraj.run()
