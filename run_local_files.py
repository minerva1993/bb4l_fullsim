#!/usr/bin/env python
import argparse
import os

def EXE(cmd, suspend=True, verbose=False, dry_run=False):
    if verbose: print colored_text('>', ['1'])+' '+cmd
    if dry_run: return

    _exitcode = os.system(cmd)

    if _exitcode and suspend: raise SystemExit(_exitcode)

    return _exitcode

WORKFLOWS_DICT = {
  'MC_bb4l_2018': [
    'files=file:INPUTFILE',
    'datasetName=BBLLNuNu_TuneCP5_13TeV-powheg-pythia8',
    'samplename=ttbartwbb4linclusive',
    'generatorName=powhegPythia',
    'outputFile=PATH/ttbartwbb4linclusive_OUTNUMBER.root',
    'pyconf=ttbartwbb4l_2018.py',
    'includePDFWeights=1',
    'includeMEWeights=1',
    'includePSWeights=0',
    'includeBFragWeights=1',
    'includeMLHdampWeights=1',
    'includeMLBFragWeights=1',
    'era=2018'
  ],
  'MC_bb4l_2018_twidthx0p7': [
    'files=file:INPUTFILE',
    'datasetName=BBLLNuNu_Width-x0p7_TuneCP5_13TeV-powheg-pythia8',
    'samplename=ttbartwbb4linclusive',
    'generatorName=powhegPythia',
    'outputFile=PATH/ttbartwbb4linclusive_0p7_widthdown_OUTNUMBER.root',
    'pyconf=ttbartwbb4l_twidthx0p7_2018.py',
    'systematicsName=WIDTH_DOWN',
    'includeMEWeights=True',
    'includePDFWeights=True',
    'includePSWeights=False',
    'includeBFragWeights=True',
    'ignoreDupl=1',
    'era=2018'
  ],
  'MC_bb4l_2018_twidthx1p3': [
    'files=file:INPUTFILE',
    'datasetName=BBLLNuNu_Width-x1p3_TuneCP5_13TeV-powheg-pythia8',
    'samplename=ttbartwbb4linclusive',
    'generatorName=powhegPythia',
    'outputFile=PATH/ttbartwbb4linclusive_1p3_widthup_OUTNUMBER.root',
    'pyconf=ttbartwbb4l_twidthx1p3_2018.py',
    'systematicsName=WIDTH_UP',
    'includeMEWeights=True',
    'includePDFWeights=True',
    'includePSWeights=False',
    'includeBFragWeights=True',
    'ignoreDupl=1',
    'era=2018'
  ],
}

### --------------------------------------------------


if __name__ == '__main__':
    ### args -----------
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('-w', '--workflows', dest='workflows', nargs='+', default=[], help='list of workflows to be executed')
    parser.add_argument('-d', '--dry-run', dest='dry_run', action='store_true', default=False, help='enable dry-run mode')
    parser.add_argument('-i', '--input', dest='input', default='/data/dust/user/jipark/production/test_root_files/008BF547-8FC3-4942-A298-DAE6AB871A18.root', help='Input file')
    parser.add_argument('-o', '--out', dest='out', default='ntple', help='Output folder')
    parser.add_argument('-n', '--outnumber', dest='outnumber', default='0', help='Input file')

    opts, opts_unknown = parser.parse_known_args()
    ### ----------------

    log_prx = os.path.basename(__file__)+' -- '

    workflows = []

    for i_wkf in opts.workflows:

        if i_wkf not in WORKFLOWS_DICT:
            print("Wrong WORKFLOW")
            sys.exit()

        workflows += [i_wkf]

    workflows = list(set(opts.workflows))

    for i_wkf in workflows:

        cmdline_args = WORKFLOWS_DICT[i_wkf]

        cmdline_args = [x.replace('INPUTFILE', opts.input).replace('OUTNUMBER', opts.outnumber).replace('PATH', opts.out) for x in cmdline_args]

        print(cmdline_args)

        cmdline_args += opts_unknown

        EXE('cmsRun ' + os.environ['CMSSW_BASE']+'/src/TopAnalysis/Configuration/analysis/common/test/ntuple_cfg.py' + ' '+(' '.join(cmdline_args)), dry_run=opts.dry_run)
