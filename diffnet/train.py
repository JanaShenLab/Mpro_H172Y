from diffnets import nnutils
from diffnets.training import Trainer
import mdtraj 
import pickle
import numpy as np

pdb = mdtraj.load('../processedTrajs/master.pdb')
n_atoms = pdb.top.n_atoms
nFeatures = int(n_atoms*3)
nearMut = mdtraj.compute_neighbors(pdb,1.,query_indices=pdb.top.select('resid 171 or resid 477'))[0]
nearMut = np.array(nearMut,dtype=int)
ind1 = nearMut*3
ind1 = np.concatenate((ind1,(nearMut*3)+1))
ind1 = np.concatenate((ind1,(nearMut*3)+2))
ind2 = np.setdiff1d(np.arange(nFeatures),ind1)
layers = [nFeatures,nFeatures,nFeatures//4,50]

params = {
        'layer_sizes' : layers,
        'em_bounds' : np.array([[0.45,0.55],[0.45,0.55]]),
        'do_em' : False,
        'em_fn' : 'em1',
        'em_batch_size' : 150,
        'em_n_cores' : 2,
        'nntype' : nnutils.split_sae,
        'lr' : 0.0001,
        'n_latent' : layers[-1],
        'act_map' : np.array([0,1],dtype=float),
        'data_dir' : '../processedTrajs/',
        'batch_size' : 32,
        'batch_output_freq' : 500,
        'epoch_output_freq' : 2,
        'test_batch_size' : 1000,
        'frac_test' : 0.1,
        'rep' : 0,
        'outdir' : 'noEM_split10',
        'subsample': 10,
        'n_epochs': 20,
        'inds1': ind1,
        'inds2': ind2
        }

trainer = Trainer(params)
net = trainer.run(data_in_mem=False)
pickle.dump(net,open('noEMSplit10_returnedNet.pkl','wb'))
