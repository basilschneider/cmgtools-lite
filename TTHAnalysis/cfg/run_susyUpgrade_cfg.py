##########################################################
##       CONFIGURATION FOR SUSY Upgrade TREES       ##
## In general all modules that are in CMGTools.TTHAnalysis.analyzers.susyCore_modules_cff
## are loaded and executed by default. Settings not overwritten here, will be taken from there.
##########################################################


import PhysicsTools.HeppyCore.framework.config as cfg

#Load all analyzers
from CMGTools.TTHAnalysis.analyzers.susyCore_modules_cff import *

#JSON
jsonAna.useLumiBlocks = True

#####Move all the definitions used through the config up here, and don't overwrite them later##########
######################################################################################################
#eleID type (cut based  = CBID)
eleID = "CBID"

# Isolation
isolation = "miniIso"
#JEC
#jetAna.mcGT = "Summer16_23Sep2016V3_MC"
##jetAna.dataGT = "Summer16_23Sep2016AllV3_DATA"
#jetAna.dataGT = "Summer16_23Sep2016BCDV3_DATA Summer16_23Sep2016EFV3_DATA Summer16_23Sep2016GV3_DATA Summer16_23Sep2016HV3_DATA"
#jetAna.runsDataJEC = [276811, 278801, 280385]
###Lets turn everything on for now, at least we know what is applied
##jetAna.addJECShifts = True
##jetAna.smearJets = False
##jetAna.recalibrateJets = True
##jetAna.applyL2L3Residual = "Data"
##metAna.recalibrate = True
###Current official recommendation for Summer16 samples: Stick with what is in MiniAOD for MC JEC
#jetAna.addJECShifts = True
#jetAna.smearJets = False
#jetAna.recalibrateJets = True
#jetAna.applyL2L3Residual = "Data"
#metAna.recalibrate = True




#-------- HOW TO RUN
#sample = 'MC'
#sample = 'data' #default
sample = 'Signal'

isData = False # default, but will be overwritten below
isSignal = False # default, but will be overwritten below
if sample == 'data':
  isData = True
elif sample == "Signal":
  isSignal = True

#Set this depending on the running mode
test = 1
#0: PRODUCTION (for batch)
#1: Usually for TESTING (single component with single thread)
#2: test all components (1 thread per comp)
#3: run all components (split jobs)
################################################################
###########################

####### Leptons  #####
# lep collection
lepAna.packedCandidates = 'packedPFCandidates'

## ELECTRONS
lepAna.loose_electron_eta = 2.4
lepAna.loose_electron_pt  = 10
lepAna.inclusive_electron_pt  = 10
if eleID == "CBID":
  lepAna.loose_electron_id  = "POG_Cuts_ID_SPRING15_25ns_v1_ConvVetoDxyDz_Veto"
  lepAna.loose_electron_lostHits = 999. # no cut since embedded in ID
  lepAna.loose_electron_dxy    = 999. # no cut since embedded in ID
  lepAna.loose_electron_dz     = 999. # no cut since embedded in ID

  lepAna.inclusive_electron_id  = "POG_Cuts_ID_SPRING15_25ns_v1_Veto"
  lepAna.inclusive_electron_lostHits = 999. # no cut since embedded in ID
  lepAna.inclusive_electron_dxy    = 999. # no cut since embedded in ID
  lepAna.inclusive_electron_dz     = 999. # no cut since embedded in ID

## MUONS
lepAna.loose_muon_pt  = 10
lepAna.inclusive_muon_pt  = 10
lepAna.loose_muon_id     = "POG_ID_Loose" #same as in core
lepAna.inclusive_muon_id     = "POG_ID_Loose" #same as in core

if isolation == "miniIso":
  # do miniIso
  lepAna.doMiniIsolation = True
  lepAna.miniIsolationPUCorr = 'rhoArea'
  lepAna.miniIsolationVetoLeptons = None
  lepAna.loose_muon_isoCut     = lambda muon : muon.miniRelIso < 0.4
  lepAna.loose_electron_isoCut = lambda elec : elec.miniRelIso < 0.4
elif isolation == "relIso03":
  # normal relIso03
  lepAna.ele_isoCorr = "rhoArea"
  lepAna.mu_isoCorr = "rhoArea"

  lepAna.loose_electron_relIso = 0.5
  lepAna.loose_muon_relIso = 0.5

########################
###### ANALYZERS #######
########################

#add LHE ana for HT info
from PhysicsTools.Heppy.analyzers.gen.LHEAnalyzer import LHEAnalyzer
LHEAna = LHEAnalyzer.defaultConfig

from CMGTools.TTHAnalysis.analyzers.ttHLepEventAnalyzer import ttHLepEventAnalyzer
ttHEventAna = cfg.Analyzer(
  ttHLepEventAnalyzer, name="ttHLepEventAnalyzer",
  minJets25 = 0,
  )

from CMGTools.TTHAnalysis.analyzers.nIsrAnalyzer import NIsrAnalyzer
NIsrAnalyzer = cfg.Analyzer(
  NIsrAnalyzer, name='NIsrAnalyzer')

#from CMGTools.RootTools.samples.triggers_13TeV_Spring15 import * # central trigger list
#from CMGTools.RootTools.samples.triggers_13TeV_Spring15_1l import *

#-------- TRIGGERS -----------
triggerFlagsAna.triggerBits = {
  }

#########################
# --- LEPTON SKIMMING ---
#########################

# GOOD LEPTON SKIMMER -- FROM TTH (in Core already)
ttHLepSkim.minLeptons = 0
ttHLepSkim.maxLeptons = 999

####### JETS #########
jetAna.jetPt = 20
jetAna.jetEta = 2.4

# --- JET-LEPTON CLEANING ---
#jetAna.cleanSelectedLeptons = True
jetAna.minLepPt = 10

## JetAna
jetAna.doQG = True

## Iso Track #use basic relIso for now
isoTrackAna.setOff = False
isoTrackAna.doRelIsolation = True

# store all taus by default
genAna.allGenTaus = True


if sample == "MC":

  print 'Going to process MC'
  print 'If It fails due to susy masses please comment out necessary lines in TTHAnalysis/python/analyzers/treeProducerSusyCore.py for now'

  from CMGTools.RootTools.samples.samples_13TeV_RunIISummer16MiniAODv2 import *

  #pick the file you want to run on
  selectedComponents = [WJetsToLNuHT]

  if test==1:
    # test a single component, using a single thread.
    comp = WJetsToLNuHT[0]
    comp.files = comp.files[:1]
    selectedComponents = [comp]
    comp.splitFactor = 1
  elif test==2:
    # test all components (1 thread per component).
    for comp in selectedComponents:
      comp.splitFactor = 1
      comp.fineSplitFactor = 1
      comp.files = comp.files[:1]
  elif test==3:
    # run all components (1 thread per component).
    for comp in selectedComponents:
      comp.fineSplitFactor = 1
      comp.splitFactor = len(comp.files)
  elif test==0:
    # PRODUCTION
    # run on everything that is defined in selectedComponents

    #selectedComponents =  [TTJets_LO , TTJets_LO_HT600to800, TTJets_LO_HT800to1200, TTJets_LO_HT1200to2500, TTJets_LO_HT2500toInf] + QCDHT + WJetsToLNuHT + SingleTop + DYJetsM50HT + TTV
    selectedComponents = WJetsToLNuHT+DiBosons+DYJetsM50HT

    for comp in selectedComponents:
      comp.fineSplitFactor = 1
      comp.splitFactor = len(comp.files)

elif sample == "Signal":

  print 'Going to process Signal, assuming it is FastSim'

  # Set FastSim JEC
  #jetAna.mcGT = "Spring16_FastSimV1_MC"

  #### REMOVE JET ID FOR FASTSIM
  jetAna.relaxJetId = True

  from private_samples import *
  #selectedComponents = [TChiWZ_300_250_miniAOD]
  selectedComponents = [TChiWZ_400_375_FullSim]

  if test==1:
    # test a single component, using a single thread.
    comp = selectedComponents[0]
    comp.files = comp.files[:1]
    selectedComponents = [comp]
    comp.splitFactor = 1
  elif test==2:
    # test all components (1 thread per component).
    for comp in selectedComponents:
      comp.splitFactor = 1
      comp.fineSplitFactor = 1
      comp.files = comp.files[:1]
  elif test==3:
    # run all components (1 thread per component).
    for comp in selectedComponents:
      comp.fineSplitFactor = 1
      comp.splitFactor = len(comp.files)
  elif test==0:
    # PRODUCTION
    # run on everything
    for comp in selectedComponents:
      comp.fineSplitFactor = 1
      comp.splitFactor = len(comp.files)



elif sample == "data":

  print 'Going to process DATA'

  # central samples
  from CMGTools.RootTools.samples.samples_13TeV_Moriond2017 import *
  #selectedComponents = [JetHT_Run2016B_23Sep2016, HTMHT_Run2016B_23Sep2016, MET_Run2016B_23Sep2016, SingleElectron_Run2016B_23Sep2016, SingleMuon_Run2016B_23Sep2016, SinglePhoton_Run2016B_23Sep2016, DoubleEG_Run2016B_23Sep2016, MuonEG_Run2016B_23Sep2016, DoubleMuon_Run2016B_23Sep2016, Tau_Run2016B_23Sep2016]
  selectedComponents = [SingleElectron_Run2016H_PromptReco_v2]
  #selectedComponents = [
  #                      SingleElectron_Run2016B_23Sep2016,\
  #                      SingleElectron_Run2016C_23Sep2016_v1,\
  #                      SingleElectron_Run2016D_23Sep2016_v1,\
  #                      SingleElectron_Run2016E_23Sep2016_v1,\
  #                      SingleElectron_Run2016F_23Sep2016_v1,\
  #                      SingleElectron_Run2016G_23Sep2016_v1,\
  #                      ]


  if test!=0 and jsonAna in susyCoreSequence: susyCoreSequence.remove(jsonAna)
  if test==1:
    # test one component (2 thread)
    comp = MET_Run2016G_23Sep2016_v1#SingleElectron_Run2016B_23Sep2016
#    comp.files = comp.files[:1]
    comp.files = comp.files[10:11]
    selectedComponents = [comp]
    comp.splitFactor = len(comp.files)
  elif test==2:
    # test all components (1 thread per component).
    for comp in selectedComponents:
      comp.splitFactor = 1
      comp.fineSplitFactor = 1
      comp.files = comp.files[10:11]
  elif test==3:
    # run all components (10 files per component).
    for comp in selectedComponents:
      comp.files = comp.files[20:30]
      comp.fineSplitFactor = 1
      comp.splitFactor = len(comp.files)
  elif test==0:
    # PRODUCTION
    # run on everything
    for comp in selectedComponents:
      comp.fineSplitFactor = 1
      comp.splitFactor = len(comp.files)



## PDF weights
PDFWeights = []

#--------- Tree Producer
from CMGTools.TTHAnalysis.analyzers.treeProducerSusyUpgrade import *
treeProducer = cfg.Analyzer(
  AutoFillTreeProducer, name='treeProducerSusyUpgrade',
  vectorTree = True,
  saveTLorentzVectors = False,  # can set to True to get also the TLorentzVectors, but trees will be bigger
  defaultFloatType = 'F', # use Float_t for floating point
  PDFWeights = PDFWeights,
  globalVariables = susyUpgrade_globalVariables,
  globalObjects = susyUpgrade_globalObjects,
  collections = susyUpgrade_collections,
  )


if isSignal:
  susyCoreSequence.insert(susyCoreSequence.index(susyScanAna)+1,
        susyCounter)
  # change scan mass parameters
  susyCounter.SUSYmodel = 'TChiWZ'
  susyCounter.SMS_mass_1 = "genSusyMNeutralino2"
  susyCounter.SMS_mass_2 = "genSusyMNeutralino"
  susyCounter.SMS_varying_masses = ['genSusyMNeutralino2','genSusyMNeutralino']

#-------- SEQUENCE
sequence = cfg.Sequence(susyCoreSequence+[
    LHEAna,
    NIsrAnalyzer,
    ttHEventAna,
    treeProducer,
    ])

if isData:
  sequence.remove(NIsrAnalyzer)
if not isSignal:
  sequence.remove(susyScanAna)

sequence.remove(genAna)
sequence.remove(genHiggsAna)
sequence.remove(genHFAna)
sequence.remove(susyScanAna)
sequence.remove(lepAna)
sequence.remove(tauAna)
sequence.remove(ttHLepSkim)
sequence.remove(photonAna)
sequence.remove(isoTrackAna)
sequence.remove(jetAna)
sequence.remove(metAna)
sequence.remove(ttHCoreEventAna)
sequence.remove(triggerFlagsAna)
sequence.remove(badMuonAna)
sequence.remove(badChargedHadronAna)
sequence.remove(NIsrAnalyzer)
sequence.remove(ttHEventAna)

#remove all skims for signal
if isSignal:
 sequence.remove(eventFlagsAna)
## output histogram
outputService=[]
from PhysicsTools.HeppyCore.framework.services.tfile import TFileService
output_service = cfg.Service(
    TFileService,
    'outputfile',
    name="outputfile",
    fname='treeProducerSusyUpgrade/tree.root',
    #fname='susyCounter/counts.root',
    option='recreate'
    )
outputService.append(output_service)

# Run Preprocessor to make MiniAOD from AOD
#from PhysicsTools.Heppy.utils.cmsswPreprocessor import CmsswPreprocessor
#preprocessor = CmsswPreprocessor('$CMSSW_BASE/src/CMGTools/TTHAnalysis/cfg/miniAOD_PAT.py')
preprocessor = None

from PhysicsTools.HeppyCore.framework.eventsfwlite import Events
config = cfg.Config( components = selectedComponents,
         sequence = sequence,
         services = outputService,
         preprocessor=preprocessor,
         events_class = Events)
