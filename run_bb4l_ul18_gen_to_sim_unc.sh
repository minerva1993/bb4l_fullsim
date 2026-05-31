#!/bin/bash

INPATH=$1
FILENUMBER=$2
SKIPEVENT=$3
MAXEVENT=$4
OUTNUMBER=$5

SCRIPT=ul18_bb4l_gen_from_lhe_recoil3.py

echo "starting"
echo "shell" $0
echo ${OUTNUMBER}
cat /etc/os-release

export SCRAM_ARCH=slc7_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh

INPUT_FOLDER=$(basename "$INPATH")

NFS_OUT_SIM=`realpath .`/out/${INPUT_FOLDER}_SIM
mkdir -p $NFS_OUT_SIM
echo ${NFS_OUT_SIM}

TMPDIR=/host/tmp
if [ ! -d ${TMPDIR} ]; then
    TMPDIR=/tmp
fi
RUNDIR=`mktemp -d -p ${TMPDIR}`
echo "Run directory: ${RUNDIR}"
cd $RUNDIR

cp /data/dust/user/jipark/production/bb4l_studies/bb4l_fullsim/ul18*.py .

# GEN: https://cms-pdmv-prod.web.cern.ch/mcm/requests?prepid=TOP-RunIISummer20UL18wmLHEGEN-00725&page=0&shown=127
cd /data/dust/user/jipark/production/bb4l_studies/CMSSW_10_6_48_pythia8313/src/run/
eval `scram runtime -sh`

if [ -f "${SCRIPT}" ]; then
    echo "File exists"
else
    cp /data/dust/user/jipark/production/bb4l_studies/bb4l_fullsim/${SCRIPT} .
fi

cmsRun "${SCRIPT}" skip=${SKIPEVENT} nEvents=${MAXEVENT} inputFiles=file:${INPATH}/LHE_${FILENUMBER}.lhe outputFile=GEN_${OUTNUMBER}.root

mv GEN_${OUTNUMBER}.root $RUNDIR/GEN.root
cd $RUNDIR

# SIM: https://cms-pdmv-prod.web.cern.ch/mcm/requests?prepid=TOP-RunIISummer20UL18SIM-00597&page=0&shown=127
scram p CMSSW CMSSW_10_6_17_patch1
cd CMSSW_10_6_17_patch1/src
eval `scram runtime -sh`

mv ../../GEN.root .
mv ../../ul18_sim.py .
cmsRun ul18_sim.py
cp SIM.root ${NFS_OUT_SIM}/SIM_${OUTNUMBER}.root
cd ../../

cd ..
rm -rf $RUNDIR
