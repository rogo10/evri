from EVRI.client import SoloClient

dum = SoloClient()
dum.clearVariables()
dum.setDataFile('c://test/test1.mat')
dum.setModelFile('c://test/plsmodel.mat')
dum.listVariables()
dum.applyModel()
dum.listVariables()
dum.getModelInfo()
print(dum.getPredictionResults())


