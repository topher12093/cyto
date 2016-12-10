import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

"""

Analysis Functionality 

- Calculate max values
- Calculate mean, rms, std1/2
- Normalize exposures
- Spatial Normalization

"""

class Analysis:

	def __init__(self, images, trials=1):
		self.trials = trials
		self.images = images
		self.maxUV = np.empty(trials)
		self.maxBlue = np.empty(trials)

	#Statistical Helper Functions

	def findMax(self):
		self.maxUV = np.max(self.images[0])
		self.maxBlue = np.max(self.images[1])
		return self.maxUV, self.maxBlue

	def calcMean(self):
		self.mean = np.mean(self.maxUV - self.maxBlue)
		return self.mean

	def calcRMS(self):
		self.RMS = np.sqrt(np.mean((self.maxUV-self.maxBlue)**2))
		return self.RMS

	def calcStdDev(self):
		self.stdUV = np.std(self.maxUV)
		self.stdBlue = np.std(self.maxBlue)
		return self.stdUV, self.stdBlue

	def calcStats(self):
		return calcMean(), calcRMS(), calcStdDev()
	
	#Plot the maximum values for UV and Blue LED	
	def generatePlots():
		plt.figure()
		plt.plot(self.maxUV,'r',label='UV')
		plt.plot(self.maxBlue,'b',label='Blue')
		plt.legend()
		plt.ylim([0,4096])

    

