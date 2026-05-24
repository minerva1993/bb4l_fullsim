from WMCore.Configuration import Configuration

config = Configuration()

config.section_('General')
config.General.requestName     = 'ul18_bb4l_lhegen'
config.General.transferOutputs = True
config.General.transferLogs    = False

config.section_('JobType')
config.JobType.pluginName  = 'PrivateMC'
config.JobType.allowUndistributedCMSSW = True 
config.JobType.psetName = 'ul18_bb4l_lhegen.py'
config.JobType.maxMemoryMB = 2500
#config.JobType.pyCfgParams = []

config.section_('User')

config.section_('Site')
config.Site.storageSite = 'T2_DE_DESY'

config.section_('Data')
config.Data.publication    = False
config.Data.ignoreLocality = False
config.Data.splitting = 'EventBased'
config.Data.outputDatasetTag = 'RunIISummer20UL18wmLHEGEN-bb4l_v2_106X_upgrade2018_realistic_v4'
config.Data.outputPrimaryDataset = 'BBLLNuNu_TuneCP5_13TeV-powheg-pythia8'
config.Data.outLFNDirBase = '/store/user/jipark/bb4l_privateSim/CR1ErdOn/UL18/LHEGEN'
config.Data.unitsPerJob = 1000
NJOBS = 5000
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS

