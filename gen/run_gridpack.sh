#!/bin/bash

NEVENTS=$1
JOBID=$2
NFILE=$3
GRIDPACK=$4

GRIDPACK=`realpath ${GRIDPACK}`
SEED1=`echo "526719+${2}+${3}" | bc`

JOBNAME=$(basename "$GRIDPACK")
JOBNAME="${JOBNAME%.*}"

echo $SEED1

PNFS_HOME="/store/user/jipark/bb4l_tests"
PNFS_OUT=${PNFS_HOME}/job_${JOBNAME}_${JOBID}

OUTDIR=`realpath .`/out/job_${JOBNAME}_${JOBID}

echo "Gridpack: ${GRIDPACK}"
echo "Output directory: ${RUNDIR}"

RUNDIR=`mktemp -d -p /host/tmp`
echo "Run directory: ${RUNDIR}"
#mkdir -p $RUNDIR
cd $RUNDIR

cat /etc/os-release

export SCRAM_ARCH=slc7_amd64_gcc700
source /cvmfs/grid.desy.de/etc/profile.d/grid-ui-env.sh

source /cvmfs/cms.cern.ch/cmsset_default.sh

export X509_USER_PROXY=~/.globus/x509up

mkdir -p $OUTDIR

tar -xf ${GRIDPACK}

./runcmsgrid.sh ${NEVENTS} ${SEED1} 1

gzip cmsgrid_final.lhe
mv cmsgrid_final.lhe.gz LHE_$NFILE.lhe.gz

echo "Generation done, copying to PNFS at ${PNFS_OUT}"

xrdfs root://dcache-cms-xrootd.desy.de mkdir ${PNFS_OUT} 
xrdcp LHE_$NFILE.lhe.gz root://dcache-cms-xrootd.desy.de/${PNFS_OUT}

if [ $? -eq 0 ]; then
    echo "Copied file successfully"
else
    echo "File copy failed, copying to NFS..."
    cp LHE_$NFILE.lhe.gz $OUTDIR
fi

cd ..
rm -rf $RUNDIR
