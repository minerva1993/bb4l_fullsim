from WMCore.Configuration import Configuration

config = Configuration()

config.section_('General')
config.General.requestName     = 'ul18_sim'
config.General.transferOutputs = True
config.General.transferLogs    = False

config.section_('JobType')
config.JobType.pluginName  = 'Analysis'
config.JobType.allowUndistributedCMSSW = True 
config.JobType.psetName = 'ul18_sim.py'
config.JobType.maxMemoryMB = 2500
config.JobType.maxJobRuntimeMin = 7200
#config.JobType.pyCfgParams = []

config.section_('User')

config.section_('Site')
config.Site.storageSite = 'T2_DE_DESY'

config.section_('Data')
config.Data.publication    = True
config.Data.ignoreLocality = False
config.Data.splitting = 'FileBased'
config.Data.inputDataset = '/BBLLNuNu_TuneCP5_13TeV-powheg-pythia8/jipark-RunIISummer20UL18reGEN_CR1ErdOn-bb4l_v2_106X_upgrade2018_realistic_v4-37bc512b6d8c546beeeb9e711198984a/USER'
config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader'
config.Data.outputDatasetTag = 'RunIISummer20UL18SIM_CR1ErdOn-bb4l_v2_106X_upgrade2018_realistic_v11_L1v1-v1'
config.Data.outLFNDirBase = '/store/user/jipark/bb4l_privateSim/CP1ErdOn/UL18/SIM'
config.Data.unitsPerJob = 1
