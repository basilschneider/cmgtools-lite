import PhysicsTools.HeppyCore.framework.config as cfg
import os
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

## FullSim AOD
#TChiWZ_300_250_FullSim = kreator.makeMCComponent('TChiWZ_300_250_FullSim', '/SMS-TChiWZ_ZToLL_mChargino-300_mLsp-250_TuneCUETP8M1_14TeV-madgraphMLM-pythia8/PhaseIIFall16DR82-PU140_90X_upgrade2023_realistic_v1-v1/AODSIM', 'CMS', '.*root', 1.0, useAAA=True)

## FullSim MiniAOD
#TChiWZ_300_250_FullSim = kreator.makeMCComponentFromLocal('TChiWZ_300_250_FullSim', 'LOCAL', 'samples2', xSec=1.0)
TChiWZ_400_375_FullSim = kreator.makeMCComponentFromLocal('TChiWZ_400_375_FullSim', 'LOCAL', '/eos/uscms/store/user/bschneid/analysis/upgrade/TChiWZ_400_375/1983785/', xSec=0.14426)
