import pypylon as pyl
import RPi.GPIO as gpio

"""

Camera

-Configures camera's properties
-Creates LED arrays
-Defines Exposures
-Sets GPIO's

"""


class Camera:

	def __init__(self):

		#Creates the device and LED's
		available_cameras = pyl.factory.find_devices()
		self.device = pyl.factory.create_device(available_cameras[0])
		self.leds = {19 : "UV", 13 : "B"} # 26 : "R"

	def configureGPIO(self):

		#Refer to the pins by Broadcom convention
		gpio.setmode(gpio.BCM)
    
    	#Set up the leds output
	    for led in self.leds:
	        gpio.setup(led,gpio.OUT)
	        gpio.output(led,gpio.LOW)

	def configureProperties(self, exposure = [1500, 1500], exposure_auto = 'Off', gain_auto = 'Off', overlap_mode = 'Off', gain = 0, pixel_format = 'Mono12'):
		
		#Configure properties of the camera for sampling.
		#This removes some of the automatic settings/modes that could interfere with testing.
		self.device.properties['ExposureTime'] = exposure
		self.device.properties['GainAuto'] = gain_auto
	    self.device.properties['OverlapMode'] = overlap_mode
	    self.device.properties['Gain'] = gain
	    self.device.properties['PixelFormat'] = pixel_format

	def listProperties(self):
		
		#Print out the property list of the camera.
		for prop in self.properties.keys():
 
	        try:
	            print(prop,end=': ')
	            print(self.properties[prop])

	        except:
	                print("Can't read")

