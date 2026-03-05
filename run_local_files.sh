#!/bin/bash

INFILE=$1
OUTFOLDER=$2
WORKFLOW=$3
OUTNUMBER=$4

echo "starting"
echo "shell" $0
echo ${INFILE}
echo ${OUTNUMBER}
cat /etc/os-release

export SCRAM_ARCH=slc7_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh

INPUT_FOLDER=$(basename "$INPATH")

cd /data/dust/user/jipark/production/CMSSW_10_6_32/src/
cmsenv
cd /data/dust/user/jipark/production/bb4l_studies/bb4l_fullsim

python run_local_files.py -w ${WORKFLOW} -i ${INFILE} -o ${OUTFOLDER} -n ${OUTNUMBER}
