from WMCore.Configuration import Configuration

config = Configuration()

config.section_('General')
config.General.requestName     = 'ul17_bb4l_lhe_from_mini'
config.General.transferOutputs = True
config.General.transferLogs    = False

config.section_('JobType')
config.JobType.pluginName  = 'Analysis'
config.JobType.allowUndistributedCMSSW = True 
config.JobType.psetName = 'ul17_bb4l_lhe_from_mini.py'
config.JobType.maxMemoryMB = 2500
#config.JobType.pyCfgParams = []

config.section_('User')

config.section_('Site')
config.Site.storageSite = 'T2_DE_DESY'

config.section_('Data')
config.Data.publication    = True
config.Data.ignoreLocality = False
config.Data.splitting = 'FileBased'
config.Data.inputDataset = '/BBLLNuNu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17MiniAODv2-bb4l_v2_106X_mc2017_realistic_v9-v2/MINIAODSIM'
config.Data.outputDatasetTag = 'RunIISummer20UL17reLHE-bb4l_v2_106X_mc2017_realistic_v6-v1'
config.Data.outLFNDirBase = '/store/user/jipark/bb4l_privateSim/LHE_nominal'
config.Data.unitsPerJob = 1
