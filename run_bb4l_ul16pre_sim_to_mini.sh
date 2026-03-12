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

cp /data/dust/user/jipark/production/bb4l_studies/bb4l_fullsim/ul16pre*.py .

# DIGIPremix: https://cms-pdmv-prod.web.cern.ch/mcm/requests?prepid=TOP-RunIISummer20UL16DIGIAPV-00026&page=0&shown=127
# CAUTION: Options are modified to use Neutrino gun samples,
# e.g. https://cms-pdmv-prod.web.cern.ch/mcm/requests?prepid=TOP-RunIISummer20UL16DIGIPremixAPV-00001&page=0&shown=127
scram p CMSSW CMSSW_10_6_17_patch1
cd CMSSW_10_6_17_patch1/src
eval `scram runtime -sh`

cp ${INPATH}/SIM_${FILENUMBER}.root ./SIM.root
mv ../../ul16pre_digipremix.py .
cmsRun ul16pre_digipremix.py
mv Premix.root ../../
cd ../../


# HLT: https://cms-pdmv-prod.web.cern.ch/mcm/requests?prepid=TOP-RunIISummer20UL16HLTAPV-00624&page=0&shown=127
export SCRAM_ARCH=slc7_amd64_gcc530
scram p CMSSW_8_0_36_UL_patch2
cd CMSSW_8_0_36_UL_patch2/src
eval `scram runtime -sh`

mv ../../ul16pre_hlt.py .
mv ../../Premix.root .
cmsRun ul16pre_hlt.py
mv HLT.root ../../
cd ../../

# RECO: https://cms-pdmv-prod.web.cern.ch/mcm/requests?prepid=TOP-RunIISummer20UL16RECOAPV-00624&page=0
# Keep using CMSSW_10_6_17_patch1
export SCRAM_ARCH=slc7_amd64_gcc700
cd CMSSW_10_6_17_patch1/src
eval `scram runtime -sh`

mv ../../HLT.root .
mv ../../ul16pre_reco.py .
cmsRun ul16pre_reco.py
mv RECO.root ../../
cd ../../

# MINIAODv2: https://cms-pdmv-prod.web.cern.ch/mcm/requests?prepid=TOP-RunIISummer20UL16MiniAODAPVv2-00600&page=0
scram p CMSSW CMSSW_10_6_25
cd CMSSW_10_6_25/src
eval `scram runtime -sh`

mv ../../RECO.root .
mv ../../ul16pre_miniv2.py .
cmsRun ul16pre_miniv2.py

mv MINIv2.root ${NFS_OUT}/MINIv2_${FILENUMBER}.root
cd ../../

cd ..
rm -rf $RUNDIR
