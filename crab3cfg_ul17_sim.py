from WMCore.Configuration import Configuration

config = Configuration()

config.section_('General')
config.General.requestName     = 'ul17_sim_EventAwareLumiBased_2'
config.General.transferOutputs = True
config.General.transferLogs    = False

config.section_('JobType')
config.JobType.pluginName  = 'Analysis'
config.JobType.allowUndistributedCMSSW = True 
config.JobType.psetName = 'ul17_sim_reshower.py'
config.JobType.maxMemoryMB = 2500
#config.JobType.maxJobRuntimeMin = 7200
#config.JobType.pyCfgParams = []

config.section_('User')

config.section_('Site')
config.Site.storageSite = 'T2_DE_DESY'

config.section_('Data')
config.Data.publication    = True
config.Data.ignoreLocality = False
config.Data.splitting = 'EventAwareLumiBased'
config.Data.inputDataset = '/BBLLNuNu_TuneCP5_13TeV-powheg-pythia8/jipark-RunIISummer20UL17reGEN_CR1ErdOn-bb4l_v2_106X_mc2017_realistic_v6-v1-389fd68e877fb00bc891148bcb1fce8c/USER'
config.Data.inputDBS = 'https://cmsweb.cern.ch/dbs/prod/phys03/DBSReader'
config.Data.outputDatasetTag = 'RunIISummer20UL17SIM_CR1ErdOn-bb4l_v2_106X_mc2017_realistic_v6-v1'
config.Data.outLFNDirBase = '/store/user/jipark/bb4l_privateSim/CR1ErdOn/UL17/SIM'
config.Data.unitsPerJob = 1000
config.Data.lumiMask = '/data/dust/user/jipark/production/bb4l_studies/bb4l_fullsim/lumimask/nominal_2.json'
