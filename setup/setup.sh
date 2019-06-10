#!/bin/sh

echo "=================================\nSETUP: data\n================================="

cd data

echo "Downloading sequence database"
wget -qO- https://sharehost.hms.harvard.edu/sysbio/alquraishi/proteinnet/sequence_dbs/proteinnet7.gz | gunzip -c > database.fa

echo "Downloading trained rgn model"
wget -c https://sharehost.hms.harvard.edu/sysbio/alquraishi/rgn_models/RGN12.tar.gz -qO - | tar -xz

echo "Setting up folder structure"
rm -rf RGN12/data/ProteinNet12Thinning90/testing/*
ln -s RGN12/data/ProteinNet12Thinning90/testing/ prediction_input
rm -rf RGN12/runs/CASP12/ProteinNet12Thinning90/11/outputsTesting/*
ln -s RGN12/runs/CASP12/ProteinNet12Thinning90/11/outputsTesting/ prediction_output
ln -s RGN12/runs/CASP12/ProteinNet12Thinning90/configuration rgn_config
mkdir workspace
mkdir archive



echo "=================================\nSETUP: rgn\n================================="

cd ..

git clone --depth=1 https://github.com/agimpel/rgn.git rgn

