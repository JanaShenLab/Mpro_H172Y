#!/bin/bash

SCRIPTS=~/Applications/rosetta_bin_linux_2017.52.59948_bundle/main/source/bin/rosetta_scripts.static.linuxgccrelease

mkdir Y172H
cd Y172H
for i in {1..40}; do 
	mkdir $i
	cd $i
	cp ../../Y172HResfile.dat ./myresfile.dat
	$SCRIPTS -s ../../H172Y_holo.pdb -parser:protocol ../../ddG-backrub.xml -in:file:fullatom -ignore_zero_occupancy false -ex1 -ex2 -extra_res_fa ../../4WI.params > rosetta.log
       	cd ../
done
