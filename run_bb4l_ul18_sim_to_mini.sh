#!/bin/bash

INPATH=$1
FILENUMBER=$2
CLUSTER=$3
PROCESS=$4

echo "starting"
echo "shell" $0
echo ${FILENUMBER}
cat /etc/os-release

export SCRAM_ARCH=slc7_amd64_gcc700
#source /cvmfs/grid.desy.de/etc/profile.d/grid-ui-env-el7.sh
export X509_USER_PROXY=/data/dust/user/jipark/production/bb4l_studies/bb4l_fullsim/x509up_u${UID}
source /cvmfs/cms.cern.ch/cmsset_default.sh
voms-proxy-info --timeleft

INPUT_FOLDER=$(basename "$INPATH")

NFS_OUT=`realpath .`/out/${CLUSTER}_${INPUT_FOLDER}_MINI
mkdir -p $NFS_OUT
echo ${NFS_OUT}

TMPDIR=/host/tmp
if [ ! -d ${TMPDIR} ]; then
    TMPDIR=/tmp
fi
RUNDIR=`mktemp -d -p ${TMPDIR}`
echo "Run directory: ${RUNDIR}"
cd $RUNDIR

cp /data/dust/user/jipark/production/bb4l_studies/bb4l_fullsim/ul18*.py .

# DIGIPremix: https://cms-pdmv-prod.web.cern.ch/mcm/requests?prepid=TOP-RunIISummer20UL18DIGIPremix-00595&page=0&shown=127
scram p CMSSW CMSSW_10_6_17_patch1
cd CMSSW_10_6_17_patch1/src
eval `scram runtime -sh`

cp ${INPATH}/SIM_${FILENUMBER}.root ./SIM.root
#mv ../../ul18_digipremix.py .
#cmsRun ul18_digipremix.py
mv ../../ul18_digipremix_IIHE.py .
cmsRun ul18_digipremix_IIHE.py
mv Premix.root ../../
cd ../../


# HLT: https://cms-pdmv-prod.web.cern.ch/mcm/requests?prepid=TOP-RunIISummer20UL18HLT-00597&page=0&shown=127
scram p CMSSW CMSSW_10_2_16_UL
cd CMSSW_10_2_16_UL/src
eval `scram runtime -sh`

mv ../../ul18_hlt.py .
mv ../../Premix.root .
cmsRun ul18_hlt.py
mv HLT.root ../../
cd ../../

# RECO: https://cms-pdmv-prod.web.cern.ch/mcm/requests?prepid=TOP-RunIISummer20UL18RECO-00597&page=0&shown=127
# Keep using CMSSW_10_6_17_patch1
cd CMSSW_10_6_17_patch1/src
eval `scram runtime -sh`

mv ../../HLT.root .
mv ../../ul18_reco.py .
cmsRun ul18_reco.py
mv RECO.root ../../
cd ../../

# MINIAODv2: https://cms-pdmv-prod.web.cern.ch/mcm/requests?prepid=TOP-RunIISummer20UL18MiniAODv2-00615&page=0&shown=127
scram p CMSSW CMSSW_10_6_20
cd CMSSW_10_6_20/src
eval `scram runtime -sh`

mv ../../RECO.root .
mv ../../ul18_miniv2.py .
cmsRun ul18_miniv2.py

mv MINIv2.root ${NFS_OUT}/MINIv2_${FILENUMBER}.root
cd ../../

cd ..
rm -rf $RUNDIR
