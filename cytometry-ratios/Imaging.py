import RPi.GPIO as gpio
import numpy as np
from scipy.ndimage import gaussian_filter
import pypylon as pyl

"""

Camera

-Configures camera's properties
-Creates LED arrays
-Defines Exposures
-Sets GPIO's

"""

"""
Still need to be debug this
"""
class Camera:

    def __init__(self):

        #Creates the device and LED's
        available_cameras = pyl.factory.find_devices()
        self.device = pyl.factory.create_device(available_cameras[0])
        self.leds = {19 : "UV", 13 : "B"} # 26 : "R"

    def configureGPIO(self):

        #Refer to the pins by Broadcom convention
        #Set up the leds output
        gpio.setmode(gpio.BCM)        

        for led in self.leds:
            gpio.setup(led,gpio.OUT)
            gpio.output(led,gpio.LOW)
            
        gpio.setup(6, gpio.IN, pull_up_down=gpio.PUD_UP)
       
    def configureProperties(self, exposure = 1500, exposure_auto = 'Off', gain_auto = 'Off', overlap_mode = 'Off', gain = 0, pixel_format = 'Mono12'):
        
        #Configure properties of the camera for sampling.
        #This removes some of the automatic settings/modes that could interfere with testing.
        self.device.open()        
        self.device.properties['ExposureTime'] = exposure
        self.device.properties['ExposureAuto'] = exposure_auto        
        self.device.properties['GainAuto'] = gain_auto
        self.device.properties['OverlapMode'] = overlap_mode
        self.device.properties['Gain'] = gain
        self.device.properties['PixelFormat'] = pixel_format

    def listProperties(self):
        
        #Print out the property list of the camera.
        for prop in self.properties.keys():

            try:
                #print(prop,end=': ')
                print(self.properties[prop])

            except:
                print("Can't read")

    def cleanUp(self):
        gpio.cleanup()
        self.close()



"""

Imaging Functionality

-Acquire Picture
-Acquire N Pictures
-Mask an image
-Clear image list
-Normalize the exposures and spatial values

"""


class Imaging(Camera):

    images = np.empty(2, int)

    def __init__(self):

        #Setup
        self.masks = []
        self.leds = {19 : "UV", 13 : "B"}
    
    def acquireImage(self, exposure, led, camera):
        camera.device.properties['ExposureTime'] = exposure
        gpio.output(led, gpio.HIGH)
        image = camera.device.grab_image()
        gpio.output(led, gpio.LOW)

        return image

    def acquireImages(self, camera, trails=1, exposures=[1500, 1500], mask=False):
        led_index = 0
        
        for i in range(trails):    
            for led in self.leds:
                self.images.append(self.acquireImage(exposures[led_index], led, camera))
                led_index+=1
                if(mask):
                    self.maskImage(mask)
            led_index = 0
            
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

        #images = acquireImages(exposure)
        ratios = self.normalizeExposure()

        normal_exp = np.asarray(exposure,int)*ratios
        normal_image = self.acquireImages(normal_exp)
        
        intensity_masks = np.ones_like(normal_image,dtype=float)  

        for i in range(len(normal_image)):
            corrected_image = gaussian_filter(normal_image[i],10).astype(float)
            max_intensity = np.max(corrected_image)
            #good_area = smooth>50
            intensity_masks[i] = max_intensity/corrected_image
        return intensity_masks        


"""
Add data or class structure for actual Image

image.Patient 
image.Date
image.Save 
"""

