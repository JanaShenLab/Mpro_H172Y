import numpy as np
import matplotlib.pyplot as plt
plt.style.use('smallFont')
plt.rcParams.update({'errorbar.capsize': 2.5})
dimerDir = 'output/dimer/'
monoDir  = 'output/monomer/'

#Read in score of each structure
scores = []
scoreTerms = []
termLabels = ['LJ attract.','LJ repul.','Solv. energy','Intra-residue repul.','Intra-residue solv. energy','Asymetric solv. energy','Elect. energy','Proline closure','Hbond, backbone','Hbond, backbone','Hbond, side.-back.','Hbond, side.-side.','Disulfide pot.','Omega dihedral','Sidechain (Dunbrack)','Torsion prob.','Tyr. hydroxyl','Ref. energy of a.a.','Rama. dihedral']
for path in [dimerDir,monoDir]:
    wtF  = open(path+'wt_.out','r')
    if(path==monoDir):
        mutF = open(path+'mut_H172Y.out','r')
    else:
        mutF = open(path+'mut_H172YH478Y.out','r')
    for label,f in zip(['WT','Mut'],[wtF,mutF]):
        totals = []
        terms = []
        for line in f:
            if('SCORE' not in line): continue
            if('score' in line): 
    #            termLabels = line.split()[2:]
                continue
            totals.append(float(line.split()[1]))
            terms.append(np.array(line.split()[2:-1],dtype=float))
        scores.append(totals)
        scoreTerms.append(terms)
#Groups: VdW, Elec., H bonds, Sovlation, other
groupedLabels = ['VdW.','Elect.','H. bonds','Solvation','Other']
groupedOrderIdx=np.array([1,2,3,0,4])

#Create figure
plt.figure(figsize=(3.5,2),tight_layout=True)
plt.ylim([-13.5,13.5])
width=.5
colors = ['grey'] + ['lightgrey']*len(groupedLabels)
#Loop over cases and plot
nTrials = len(scores[0])
patterns = ['','///']
for i,(wtIdx,mutIdx) in enumerate(zip([0,2],[1,3])):
    pattern=patterns[i]
    diffScore = np.mean(scores[mutIdx],axis=0)-np.mean(scores[wtIdx],axis=0)
    stdScore = np.std([mut-wt for wt,mut in zip(scores[wtIdx],scores[mutIdx])])
    diffTerms = np.mean(scoreTerms[mutIdx],axis=0)-np.mean(scoreTerms[wtIdx],axis=0)
    stdTerms = np.std([mut-wt for wt,mut in zip(scoreTerms[wtIdx],scoreTerms[mutIdx])],axis=0)
    groupedTerms = np.array([np.sum(diffTerms[[0,1,3]]),diffTerms[6],np.sum(diffTerms[[8,9,10,11]]),np.sum(diffTerms[[2,4,5]]),np.sum(diffTerms[[7,12,13,14,15,16,17,18]])])
    groupedTermErrors = np.array([np.sum(stdTerms[[0,1,3]]),stdTerms[6],np.sum(stdTerms[[8,9,10,11]]),np.sum(stdTerms[[2,4,5]]),np.sum(stdTerms[[7,12,13,14,15,16,17,18]])])/np.sqrt(nTrials)
    #Scale monomer to dimer
    if(i==1):
        diffScore*=2
        stdScore*=2
        groupedTerms*=2
        groupedTermErrors*=2
    print(diffScore,stdScore/np.sqrt(nTrials))
    print(groupedLabels)
    print(groupedTerms)
    print(groupedTermErrors)
    plt.bar(
            (i-1)*width+np.arange(-1,len(groupedLabels)),
            np.concatenate(([diffScore],groupedTerms[groupedOrderIdx])),
            width=width,color=colors,align='edge',
            yerr=np.concatenate(([stdScore]/np.sqrt(nTrials),groupedTermErrors)),
            linewidth=1.75,edgecolor='black',
            hatch=pattern)
plt.legend(['Dimer','Monomers'])
plt.xticks(range(-1,len(groupedLabels)),['Total']+[groupedLabels[i] for i in groupedOrderIdx],rotation=-45,ha='left',rotation_mode='anchor')
plt.ylabel('$\mathrm{\Delta\Delta G_{fold}}$ (kcal/mol)')
plt.axhline(y=0,c='black')
plt.savefig('Figure3.pdf')
plt.show()
