from diffnets.analysis import Analysis
import pickle

data_dir = '../processedTrajs/'
outdir = 'analysis_noEM10'
net = pickle.load(open('noEMSplit10_returnedNet.pkl','rb'))

#Load network into cpu memory
net.cpu()

a = Analysis(net,outdir,data_dir)
a.run_core()
