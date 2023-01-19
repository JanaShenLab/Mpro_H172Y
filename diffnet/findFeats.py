from diffnets.analysis import Analysis
import pickle
import mdtraj
import numpy as np

data_dir = '../processedTrajs/'
outdir = 'analysis_noEM10'
net = pickle.load(open('noEMSplit10_returnedNet.pkl','rb'))
pdb = mdtraj.load('../processedTrajs/master.pdb')

#Load network into cpu memory
net.cpu()

nearMut = mdtraj.compute_neighbors(pdb,1.5,query_indices=pdb.top.select('resid 171 or resid 477 and name CA'),haystack_indices=pdb.top.select('name CA'))[0]

a = Analysis(net,outdir,data_dir)
a.find_feats(nearMut,"corr-50_close.pml",n_states=200,num2plot=50)
