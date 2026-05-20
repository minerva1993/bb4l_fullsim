BASE="/pnfs/desy.de/cms/tier2/store/user/jipark/bb4l_privateSim/LHE_nominal/BBLLNuNu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16reLHE-bb4l_v2_106X_mcRun2_asymptotic_v13-v1/260505_124028"

QUEUE_LINES=$(find "$BASE" -name "LHE_*.root" | awk -F'/' '{
    A=$(NF-1)
    B=$NF
    sub(/LHE_/, "", B)
    sub(/\.root/, "", B)
    print A ", " B
}' | sort)

cat > job.sub << EOF
JobBatchName = "ul16post_bb4l_lhe_from_mini_plainLHE"
Executable  = /data/dust/user/jipark/production/bb4l_studies/bb4l_fullsim/run_edm_to_lhe.sh
Log         = /data/dust/user/jipark/production/bb4l_studies/bb4l_fullsim/logs/log_\$(Cluster)_\$(Process).txt
Output      = /data/dust/user/jipark/production/bb4l_studies/bb4l_fullsim/logs/out_\$(Cluster)_\$(Process).txt
Error       = /data/dust/user/jipark/production/bb4l_studies/bb4l_fullsim/logs/err_\$(Cluster)_\$(Process).txt
Args        = "UL16 /pnfs/desy.de/cms/tier2/store/user/jipark/bb4l_privateSim/LHE_nominal/BBLLNuNu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16reLHE-bb4l_v2_106X_mcRun2_asymptotic_v13-v1/260505_124028 \$(A) \$(B)"
+RequestRuntime = 3600
RequestMemory = 2048
RequestCpus = 1
Request_OpSysAndVer = "RedHat9"
+CondorPlatform = "\$CondorPlatform: x86_64_RedHat9 \$"
+MySingularityImage = "/cvmfs/unpacked.cern.ch/registry.hub.docker.com/cmssw/cc7:x86_64"
+MySingularityArgs = "--bind /tmp:/host/tmp --bind /etc/pki/ca-trust --bind /cvmfs/grid.cern.ch/etc/grid-security:/etc/grid-security --bind  /cvmfs/grid.cern.ch/etc/grid-security/vomses:/etc/vomses"

queue A, B from (
${QUEUE_LINES}
)
EOF

echo "Generated job.sub with $(echo "$QUEUE_LINES" | wc -l) jobs"
