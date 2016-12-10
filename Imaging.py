import RPi.GPIO as gpio
from Camera import *

"""

Imaging Functionality

-Acquire Picture
-Acquire N Pictures
-Mask an image
-Clear image list
-Normalize the exposures and spatial values

"""


class Imaging(Camera):


	def __init__(self, cam):

		#Create image list
		self.images = []
		self.cam = cam
	
	def acquireImage(self, exposure=[1500, 1500]):

		self.cam.properties['ExposureTime'] = exposure
		gpio.output(led, gpio.HIGH)
		self.image = self.grab_image()
		gpio.output(led, gpio.LOW)

		return self.image

	def acquireImages(self, exposure=[1500, 1500], trails=1, mask=False):
		for i in range(trials):	
			for led in self.leds:
				self.images.append(acquireImage(led))
				if(masks):
					maskImage(masks)


		return self.images

	def maskImage(self, masks):
		self.images[0] = self.images[0]*masks[0]
		self.images[1] = self.images[1]*masks[1]

		return self.images

	def clearImages(self):
		self.images[:] = []


	#Normalization Functions

	def normalizeExposure(self, variance=10):
		normalized_exp = np.empty(2,float)
		max_intensities = np.empty(2,int)

		for i in range(len(self.images)):
			self.images = gaussian_filter(self.images[i],variance).astype(float)
			max_intensity = np.max(self.images)
			max_intensities[i] = max_intensity

			normalized_exp[0] = 1.0
			normalized_exp[1] = max_intensities[0]/max_intensities[1]

			return normalized_exp

	def normalizeSpatial(self, exposure=[500,500]):

	    images = acquireImages(exposure)
	    ratios = normalizeExposure()

	    normal_exp = np.asarray(exposure,int)*ratios
	    normal_image = acquireImages(normal_exp)
	    
	    intensity_masks = np.ones_like(normal_image,dtype=float)  

	    for i in range(len(normal_image)):
	        corrected_image = gaussian_filter(normal_image[i],10).astype(float)
	        max_intensity = np.max(corrected_image)
	        #good_area = smooth>50
	        intensity_masks[i] = max_intensity/corrected_image
	    return intensity_masks        


