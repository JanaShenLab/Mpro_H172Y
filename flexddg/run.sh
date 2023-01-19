#!/bin/bash

SCRIPTS=~/Applications/rosetta_bin_linux_2017.52.59948_bundle/main/source/bin/rosetta_scripts.static.linuxgccrelease

mkdir H172Y
cd H172Y
for i in {1..40}; do 
	mkdir $i
	cd $i
	cp ../../H172YResfile.dat ./myresfile.dat
	$SCRIPTS -s ../../wt_holo.pdb -parser:protocol ../../ddG-backrub.xml -in:file:fullatom -ignore_zero_occupancy false -ex1 -ex2 -extra_res_fa ../../4WI.params > rosetta.log
       	cd ../
done
