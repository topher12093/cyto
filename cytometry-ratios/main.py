from LCD import *
from Imaging import *
from Camera import *
from Analysis import *



if __name__ == '__main__':


	#	1. SET UP

	#Set up Camera
	cam = Camera()
	cam.configureGPIO()
	cam.configureProperties()

	#Setup LCD
	lcd = LCD()


	#	2. IMAGING

	#Begin the Imaging Sequence
	#Normalize Exposure and Spatial values
	images = Imaging(cam)
	images.acquireImages()
	image_masks = images.normalizeSpatial()

	#Apply mask generated by normalization
	masked_image = images.maskImage(image_masks)




	#	3. Analysis

	#Calculate stats and plot
	stats = Analysis(masked_image)
	stats.findMax()
	stats.calcStats()
	stats.generatePlots()


	#   4. Cleanup
	cam.cleanUp()