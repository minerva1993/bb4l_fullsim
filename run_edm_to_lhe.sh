#!/bin/bash

ERA=$1
INPATH=$2
FOLDERNUMBER=$3
FILENUMBER=$4

echo "starting"
echo "shell" $0
echo ${FILENUMBER}
cat /etc/os-release

export SCRAM_ARCH=slc7_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh

INPUT_FOLDER=$(basename "$INPATH")

NFS_OUT_SIM=`realpath .`/out/LHE_Nominal_${ERA}/${FOLDERNUMBER}
mkdir -p $NFS_OUT_SIM
echo ${NFS_OUT_SIM}

TMPDIR=/host/tmp
if [ ! -d ${TMPDIR} ]; then
    TMPDIR=/tmp
fi
RUNDIR=`mktemp -d -p ${TMPDIR}`
echo "Run directory: ${RUNDIR}"
cd $RUNDIR


scram p CMSSW CMSSW_10_6_40
cd CMSSW_10_6_40/src
eval `scram runtime -sh`

cp /data/dust/user/jipark/production/bb4l_studies/bb4l_fullsim/bb4l_lhe_from_mini_plainLHE.py .
cmsRun bb4l_lhe_from_mini_plainLHE.py inputFiles=file:${INPATH}/${FOLDERNUMBER}/LHE_${FILENUMBER}.root
cp writer.lhe ${NFS_OUT_SIM}/LHE_${FILENUMBER}.lhe

cd ../../../

rm -rf $RUNDIR
