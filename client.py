import requests as r
import xml.etree.ElementTree as ET
import re
import numpy as np

class SoloClient:


	"""
	Initialize object of class SoloClient.
	Port defaults to 2211.
	Variables pathDataFile, pathModelFile, pathIncludeFile, errorString are empty strings as default.
	IPAddress default is 127.0.0.1.
	resultsOutputFormat is str (default='dict')
	outputKeys will be [] to start.


	General flow of object...

	-------	instance = SoloClient()		creates instance
	-------	instance.setDataFile(path)	creates var, data, in Solo workspace equal to path, accessible by calling instance.getDataFile()
	-------	instance.setModelFile(path)	creates var, model, in workspace equal to file, accessible by calling instance.getDataFile()
	-------	instance.applyModel()		applies <pred=model|data> in workspace (creates var, pred)
		

	-------	instance.clearVariables()	clears workspace
	-------	instance.listVariables()	returns python list of vars in workspace
		


	"""
	
	def __init__(self):
		
		#define a session and other private variables with default values
	
		self._session = r.Session()
		self._port=2211
		self._IPAddress = '127.0.0.1'
		self._pathModelFile = ''
		self._pathDataFile = ''
		self._pathIncludeFile = ''
		self._errorString = ''
		self._resultsOutputFormat = 'dict'
		self._response = ''
		self._outputKeys = []
		self._versionMode = 'notfull'
		
	#############methods###############
		
	def clearVariables(self):

		#uses url for clearing command and session will execute the url to clear variables.

		urlClear = "http://"+str(self._IPAddress)+":"+str(self._port)+"/?:clear;"
	
		if(self._session.get(urlClear)):
			return True
		else:
			return False
	
	def listVariables(self):

		#uses url for list command and session will execute the url to list variables.

		urlList = "http://"+str(self._IPAddress)+":"+str(self._port)+"/?:plain;:list;"
		request = self._session.get(urlList)
		if(request):
			print([element for element in request.text.split('\n') if element != ''])
			return True
		else:
			return False

	def applyModel(self):
		
		#apply pred= model|data, also update the outputKeys to workspace, command executed in url parameter.

		urlApply = """http://"""+str(self._IPAddress)+""":"""+str(self._port)+"""/?pred = model|data;"""
		if(self._session.get(urlApply)):
			keysNotCleaned = []
			self._outputKeys = []
			urlGetOutputKeys = """http://"""+str(self._IPAddress)+""":"""+str(self._port)+"""/?pred.plotscores;"""
			tree = ET.fromstring(self._session.get(urlGetOutputKeys).text)
			for child in tree.iter('sr'):
				keysNotCleaned.append(child.text)
			for key in keysNotCleaned:
				try:
					self._outputKeys.append(re.match(r'^(.*)\s+\([0-9\.%]+\)+\s+$',key).group(1))
				except AttributeError:
					self._outputKeys.append(key)
			return True
		else:
			return False


	####################Setters######################

	def setDataFile(self,path):

		#updates private var for data file
		#conditions on :plain text upon workspace <data> variable definition, if no text load was successful

		self._pathDataFile = path
		urlsetDataFile = """http://"""+str(self._IPAddress)+""":"""+str(self._port)+"""/?:plain;data="""+str("'")+self._pathDataFile+str("'")+""";"""	
	
		dataText = self._session.get(urlsetDataFile).text.split('\n')
		if(dataText==['','']):

			return True
		else:
			return False

	def setModelFile(self,path):

		#updates private var for model file
		#conditions much like self.setDataFile()

		self._pathModelFile = path
		urlSetModelFile = """http://"""+str(self._IPAddress)+""":"""+str(self._port)+"""/?:plain;model="""+str("'")+self._pathModelFile+str("'")+""";"""
		modelText = self._session.get(urlSetModelFile).text.split('\n')
		
		if(modelText==['','']):
			return True
		else:
			return False
		urlGetModelInfo = """http://"""+str(self._IPAddress)+""":"""+str(self._port)+"""/?model.info;"""
	
	def setOutputFormat(self,format):
	
		#updates private var for output format of pred.plotscores
		#checks if format=='dict' or 'xml', raises ValueError otherwise	

		if(format in ['dict', 'xml']):
			self._resultsOutputFormat = format
		else:
			raise ValueError("Output format must be either 'dict' or 'xml'")

	def setPort(self,num):
	
		#updates private var for port		
		#checks if port in [1,65535], raises ValueError if not in range (code says 65536 but this value is not included when checking port
	
		if(num in [i for i in range(1,65536)]):
			self._port = num
			return True
		else:
			raise ValueError("Port number, ",num, "not in [1,65535].")
	
	def setIPAddress(self,value):
	
		#updates private var for IP Address
		#checks if address is formatted correctly, returns True if correct and False otherwise

		address = value.split(".")
		address = [element for element in address if element != '']
		if(len(address)!=4):
			raise ValueError('Your input, ',value, ' does not follow the IPAddress format standards.')
		for num in address:
			if(num not in [i for i in range(0,256)]):
				return False
			else:
				pass
		self._IPAddress = value
		return True

	
	
	###################getters######################
	
	def getDataFile(self):
		return self._pathDataFile

	def getModelFile(self):
		return self._pathModelFile
	
	def getPort(self):
		return self._port

	def getIPAddress(self):
		return self._IPAddress
	
	def getOutputFormat(self):
		return self._resultsOutputFormat

	def getPredictionResults(self):

		#returns results
		#dict if ouput format=='dict'
		#xml string if output format=='xml'
		#raises ValueError if output format not either 'dict' or 'xml'

		keysNotCleaned = []
		self._outputKeys = []
		urlGetResults = """http://"""+str(self._IPAddress)+""":"""+str(self._port)+"""/?pred.plotscores;"""
		tree = ET.fromstring(self._session.get(urlGetResults).text)
		for child in tree.iter('sr'):
			keysNotCleaned.append(child.text)
		for key in keysNotCleaned:
			try:
				self._outputKeys.append(re.match(r'^(.*)\s+\([0-9\.%]+\)+\s+$',key).group(1))
			except AttributeError:
				self._outputKeys.append(key)
		if(self._resultsOutputFormat == 'xml'):
			return(self._session.get(urlGetResults).text)
		elif(self._resultsOutputFormat == 'dict'):
			obs = []
			mydict = {}
			for child in tree.iter('data'):
				obs.append(child.text)
				myshape = child.get('size')
			scores = obs[0].replace('\n','').replace(';',',')
			scores = np.array([float(element) for element in scores.split(',')])
			scores = scores.reshape(eval(myshape))
			#get shape
			colNum = 0
			for key in self._outputKeys:
				mydict[key] = scores[:][colNum]
				colNum+=1
			return mydict
		else:
			raise ValueError("Results format must either be 'dict' or 'xml'.")

			
			

	
	def getModelInfo(self):

		#returns xml string from executing model.info

		urlModelInfo = """http://"""+str(self._IPAddress)+""":"""+str(self._port)+"""/?model.info;"""
		tree = ET.fromstring(self._session.get(urlModelInfo).text)
		modelInfo = ''
		for child in tree.iter('td'):
			modelInfo = modelInfo+str(child.text)+'\n'
		return modelInfo

	def getPredictionResultsVarNames(self):
		return self._outputKeys

	def getVersion(self,mode='notfull'):
	
		#returns version info from executing :version
			#xml string if mode=='full'
			#dict if mode=='notfull' (default)	

		urlVersion = """http://"""+str(self._IPAddress)+""":"""+str(self._port)+"""/?:version;"""
		versionText = ''
		versionDict = {}
		if(mode=='full'):
			#need release, matlab version, license
			versionText = self._session.get(urlVersion).text
			return versionText
		elif(mode=='notfull'):
			versionText = self._session.get(urlVersion).text.split('\n')[2:5]
			versionDict['License'] = re.match(r'^License:\s+(.*)$',versionText[0]).group(1)
			versionDict['Release'] = re.match(r'^Release:\s+(.*)$',versionText[1]).group(1)
			versionDict['Matlab Version'] = re.match(r'^MatlabVersion:\s+(.*)$',versionText[2]).group(1)

			return versionDict
		else:
			raise ValueError("To access all version information, pass 'full', default version dictionary will be returned otherwise.")
		










