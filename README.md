# Note: Some config might be modified from the original commands

## test command

./run_bb4l_ul18_gen_to_sim.sh /data/dust/user/jipark/production/CMSSW_10_6_39/src/genproductions/bin/Powheg/out/job_b_bbar_4l_slc7_amd64_gcc700_CMSSW_10_6_39_bb4l_dl_twidthx0p7_allflavors_3_3899782 12345 0


## Submit GEN-SIM

python write_split_SIM_script.py -I /data/dust/user/jipark/production/CMSSW_10_6_39/src/genproductions/bin/Powheg/out/job_b_bbar_4l_slc7_amd64_gcc700_CMSSW_10_6_39_bb4l_dl_twidthx0p7_allflavors_3_3896071 -Y ul18 -W 0p7 -M 1000

python write_split_SIM_script.py -I /data/dust/user/jipark/production/CMSSW_10_6_39/src/genproductions/bin/Powheg/out/job_b_bbar_4l_slc7_amd64_gcc700_CMSSW_10_6_39_bb4l_dl_twidthx1p3_allflavors_3_3896070 -Y ul18 -W 1p3 -M 1000


###  resubmitted jobs
grep -rl -e 'Fatal Exception' -e 'atal system signal' logs/err_1734472_*_2.txt | python write_resubmit_script.py -I submit_bb4l_width0p7_gen_to_sim_ul18

grep -rl -e 'Fatal Exception' -e 'atal system signal' logs/err_1727291_*_2.txt | python write_resubmit_script.py -I submit_bb4l_width1p3_gen_to_sim_ul18

python checkRootFiles.py -I out/OUTFOLDER

python write_resubmit_script.py -I submit_bb4l_width0p7_gen_to_sim_ul18 -O out/1837091_job_b_bbar_4l_slc7_amd64_gcc700_CMSSW_10_6_39_bb4l_dl_twidthx0p7_allflavors_3_732555_SIM/

!!!!!!!!Remove files and run resubmission!!!!!!!!!!

gfal-copy -r job_b_bbar_4l_slc7_amd64_gcc700_CMSSW_10_6_39_bb4l_dl_twidthx1p3_allflavors_3_3896070_SIM  "davs://dcache-cms-webdav.desy.de:2880/pnfs/desy.de/cms/tier2/store/user/jipark/bb4l_fullsim/SIM/job_b_bbar_4l_slc7_amd64_gcc700_CMSSW_10_6_39_bb4l_dl_twidthx1p3_allflavors_3_3896070_SIM" -t 29600

rsync -rlnv job_b_bbar_4l_slc7_amd64_gcc700_CMSSW_10_6_39_bb4l_dl_twidthx1p3_allflavors_3_3896070_SIM/ /pnfs/desy.de/cms/tier2/store/user/jipark/bb4l_fullsim/SIM/job_b_bbar_4l_slc7_amd64_gcc700_CMSSW_10_6_39_bb4l_dl_twidthx1p3_allflavors_3_3896070_SIM/ --delete --dry-run --ignore-existing

python checkRootFiles.py -I /pnfs/desy.de/......


## Submit Premix - Mini

source setup.sh

python write_mini_script.py -I /pnfs/desy.de/cms/tier2/store/user/jipark/bb4l_fullsim/SIM/job_b_bbar_4l_slc7_amd64_gcc700_CMSSW_10_6_39_bb4l_dl_twidthx0p7_allflavors_3_712586_SIM -Y ul18 -W 0p7

python write_mini_script.py -I /pnfs/desy.de/cms/tier2/store/user/jipark/bb4l_fullsim/SIM/job_b_bbar_4l_slc7_amd64_gcc700_CMSSW_10_6_39_bb4l_dl_twidthx1p3_allflavors_3_712587_SIM -Y ul18 -W 1p3



grep -rl -e 'Fatal Exception' -e 'atal system signal' -e 'mv: cannot stat' logs/err_1751936_*_2.txt | python write_resubmit_script.py -I submit_bb4l_width0p7_sim_to_mini_ul18

grep -rl -e 'Fatal Exception' -e 'atal system signal' -e 'mv: cannot stat' logs/err_1768772_*_2.txt | python write_resubmit_script.py -I submit_bb4l_width1p3_sim_to_mini_ul18

(IF missing files exist...)

python write_resubmit_script.py -I submit_bb4l_width1p3_sim_to_mini_ul18 -O out/

python checkRootFiles.py -I out/1751936


## To merge several MiniAOD files together:
python write_edm_merge_script.py -I out/job_b_bbar_4l_slc7_amd64_gcc700_CMSSW_10_6_39_bb4l_dl_twidthx0p7_allflavors_3_712586_SIM_MIN


## To Ntuple
python run_local_files.py -w MC_bb4l_2018_twidthx1p3 -i /data/dust/user/jipark/production/bb4l_studies/bb4l_fullsim/out/job_b_bbar_4l_slc7_amd64_gcc700_CMSSW_10_6_39_bb4l_dl_twidthx1p3_allflavors_3_3896070_SIM_MINI/MINIv2_0.root -o ntuple_twidthx1p3 -n 0

python write_ntuple_script.py -Y ul18 --workflow MC_bb4l_2018_twidthx0p7 -W 0p7 -O ntuple_twidthx0p7 -I miniaodv2_twidthx0p7

python write_ntuple_script.py -Y ul18 --workflow MC_bb4l_2018_twidthx1p3 -W 1p3 -O ntuple_twidthx1p3 -I miniaodv2_twidthx1p3

python write_ntuple_merge_script.py -I ntuple_twidthx1p3
