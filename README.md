test command

./run_bb4l_ul18_gen_to_sim.sh /data/dust/user/jipark/production/CMSSW_10_6_39/src/genproductions/bin/Powheg/out/job_b_bbar_4l_slc7_amd64_gcc700_CMSSW_10_6_39_bb4l_dl_twidthx0p7_allflavors_3_3899782 12345 0



python write_split_SIM_script.py -I /data/dust/user/jipark/production/CMSSW_10_6_39/src/genproductions/bin/Powheg/out/job_b_bbar_4l_slc7_amd64_gcc700_CMSSW_10_6_39_bb4l_dl_twidthx0p7_allflavors_3_3896071 -Y ul18 -W 0p7 -M 1000

python write_split_SIM_script.py -I /data/dust/user/jipark/production/CMSSW_10_6_39/src/genproductions/bin/Powheg/out/job_b_bbar_4l_slc7_amd64_gcc700_CMSSW_10_6_39_bb4l_dl_twidthx1p3_allflavors_3_3896070 -Y ul18 -W 1p3 -M 1000

Events->Scan("GenEventInfoProduct_generator__GEN.obj.weights_")

grep -rl 'EEEE ------- G4Exception-START'
grep -rl 'WrongFileFormat'
grep -rIl -L "RunIISummer20ULPrePremix" err_870259_* 
grep -rIl "Fatal Exception" err_870259_* | xargs grep -L "RunIISummer20ULPrePremix"

condor_q -hold -format "%d_" ClusterId -format "%d " ProcId -format "%s\n" HoldReason

condor_rm -const 'jobstatus==5'


#for SIM / resubmitted jobs
#Not having BOTH expressions
grep -rl -L -e 'Fatal Exception' -e 'fatal system signal' logs/err_894272_*

grep -rl -e 'Fatal Exception' -e 'atal system signal' logs/err_1726953_*

grep -rl -e 'Fatal Exception' -e 'atal system signal' logs/err_1734472_*_2.txt | python write_resubmit_script.py -I submit_bb4l_width0p7_gen_to_sim_ul18

grep -rl -e 'Fatal Exception' -e 'atal system signal' logs/err_1727291_*_2.txt | python write_resubmit_script.py -I submit_bb4l_width1p3_gen_to_sim_ul18

python checkRootFiles.py -I out/

python write_resubmit_script.py -I submit_bb4l_width0p7_gen_to_sim_ul18 -O out/1837091_job_b_bbar_4l_slc7_amd64_gcc700_CMSSW_10_6_39_bb4l_dl_twidthx0p7_allflavors_3_732555_SIM/

!!!!!!!!Remove files and run resubmission!!!!!!!!!!


gfal-copy -r job_b_bbar_4l_slc7_amd64_gcc700_CMSSW_10_6_39_bb4l_dl_twidthx1p3_allflavors_3_3896070_SIM  "davs://dcache-cms-webdav.desy.de:2880/pnfs/desy.de/cms/tier2/store/user/jipark/bb4l_fullsim/SIM/job_b_bbar_4l_slc7_amd64_gcc700_CMSSW_10_6_39_bb4l_dl_twidthx1p3_allflavors_3_3896070_SIM" -t 29600

rsync -rlnv job_b_bbar_4l_slc7_amd64_gcc700_CMSSW_10_6_39_bb4l_dl_twidthx1p3_allflavors_3_3896070_SIM/ /pnfs/desy.de/cms/tier2/store/user/jipark/bb4l_fullsim/SIM/job_b_bbar_4l_slc7_amd64_gcc700_CMSSW_10_6_39_bb4l_dl_twidthx1p3_allflavors_3_3896070_SIM/ --delete --dry-run --ignore-existing

python checkRootFiles.py -I /pnfs/desy.de/cms/tier2/store/user/jipark/bb4l_fullsim/SIM/job_b_bbar_4l_slc7_amd64_gcc700_CMSSW_10_6_39_bb4l_dl_twidthx0p7_allflavors_3_712586_SIM


////////////////// Premix - Mini ///////////////////

source setup.sh #!!!!!!!!!!!!!!!!

python write_mini_script.py -I /pnfs/desy.de/cms/tier2/store/user/jipark/bb4l_fullsim/SIM/job_b_bbar_4l_slc7_amd64_gcc700_CMSSW_10_6_39_bb4l_dl_twidthx0p7_allflavors_3_712586_SIM -Y ul18 -W 0p7

python write_mini_script.py -I /pnfs/desy.de/cms/tier2/store/user/jipark/bb4l_fullsim/SIM/job_b_bbar_4l_slc7_amd64_gcc700_CMSSW_10_6_39_bb4l_dl_twidthx1p3_allflavors_3_712587_SIM -Y ul18 -W 1p3



grep -rl -e 'Fatal Exception' -e 'atal system signal' -e 'mv: cannot stat' logs/err_1751936_*_2.txt | python write_resubmit_script.py -I submit_bb4l_width0p7_sim_to_mini_ul18

grep -rl -e 'Fatal Exception' -e 'atal system signal' -e 'mv: cannot stat' logs/err_1768772_*_2.txt | python write_resubmit_script.py -I submit_bb4l_width1p3_sim_to_mini_ul18

IF!! missing files exist...

python write_resubmit_script.py -I submit_bb4l_width1p3_sim_to_mini_ul18 -O out/

python checkRootFiles.py -I out/1751936


grep -rl -L -e "Closed file file:RECO.root" logs/err_1734472_*_2.txt | python write_resubmit_script.py -I submit_bb4l_width0p7_sim_to_mini_ul18



To merge several files together:


edmCopyPickMerge inputFiles=first.root,second.root,third.root outputFile=output.root maxSize=1000000
where the input files are first.root, second.root, and third.root and the output file is output.root or


edmCopyPickMerge inputFiles_load=listOfInputFiles.txt outputFile=output.root maxSize=1000000
where listOfInputFiles.txt is a text file containing a list of input files (one file per line) and output.root is the output file and 1000000 is the maximum size of the output file in Kb (e.g., 1000000 Kb = 1 Gb).

