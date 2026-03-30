#!/bin/bash

NEVENTS=$1
JOBID=$2
NFILE=$3
GRIDPACK=$4

GRIDPACK=`realpath ${GRIDPACK}`
SEED1=`echo "526719+${2}+${3}" | bc`

JOBNAME=$(basename "$GRIDPACK")
JOBNAME="${JOBNAME%.*}"

klist
echo $KRB5CCNAME

echo $SEED1

OUTDIR=/cms/ldap_home/minerva1993/bb4l_fullsim/gen/out/job_${JOBNAME}_${JOBID}

RUNDIR=`mktemp -d -p /tmp`
echo "Run directory: ${RUNDIR}"
#mkdir -p $RUNDIR
cd $RUNDIR

export SCRAM_ARCH=slc7_amd64_gcc700

source /cvmfs/cms.cern.ch/cmsset_default.sh

export X509_USER_PROXY=/cms/ldap_home/minerva1993/bb4l_fullsim/x509up_u${UID}

mkdir -p $OUTDIR

tar -xf ${GRIDPACK}

./runcmsgrid.sh ${NEVENTS} ${SEED1} 1

gzip cmsgrid_final.lhe
mv cmsgrid_final.lhe.gz LHE_$NFILE.lhe.gz

echo "Generation done, copying to home at ${OUTDIR}"

cp LHE_$NFILE.lhe.gz $OUTDIR

cd ..
rm -rf $RUNDIR
