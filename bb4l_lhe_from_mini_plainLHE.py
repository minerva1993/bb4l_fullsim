import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing

options = VarParsing('analysis')
options.parseArguments()

process = cms.Process('Writer')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.EndOfProcess_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring (options.inputFiles)
)

process.options = cms.untracked.PSet(

)

process.writer = cms.EDAnalyzer('LHEWriter')
process.writer.moduleLabel = cms.untracked.InputTag('externalLHEProducer')

# Path and EndPath definitions
process.endjob_step = cms.EndPath(process.endOfProcess)
process.LHEoutput_step = cms.EndPath(process.writer)

# Schedule definition
process.schedule = cms.Schedule(process.endjob_step,process.LHEoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring 

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

process.MessageLogger.cerr.FwkReport.reportEvery=500
