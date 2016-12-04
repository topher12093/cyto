import numpy as np
import matplotlib.pyplot as plt
import pypylon as pyl
import RPi.GPIO as gpio
from scipy.ndimage import gaussian_filter
import Adafruit_CharLCD as LCD

from time import time,sleep
import gaugette.rotary_encoder

#Takes a raw image with the camera at a specified exposure time and returns the image
def acquire(cam,exposure_time,led_pin):
    cam.properties['ExposureTime'] = exposure_time
    gpio.output(led_pin,gpio.HIGH)
    image = cam.grab_image()
    gpio.output(led_pin,gpio.LOW)
    return image
    
#Prints the properties of the camera   
def listProperties(cam):
    for prop in cam.properties.keys():
        try:
            print(prop,end=': ')
            print(cam.properties[prop])
        except:
                print("Can't read")

#Clean's up GPIO's and closes the camera
def end():
    gpio.cleanup()
    cam.close()
  

#Calculates the mean, rms, standard deviations   
def calcVar(cam,exposures,trials):
    
    #Pass number of images to take
    TRIALS = trials
    
    #Specify which LED's we're using
    led = [19, 13]
    
    #Max value arrays to store the max value of each image caputre
    maxvals = np.empty(TRIALS)
    maxvals2 = np.empty(TRIALS)

    #Take images for the amount of specified trials.
    #Finds the max of each image and uses it to calculate stats

    for i in range(TRIALS):
        images = takePics(cam,led,exposures)
        maxvals[i] = np.max(images[0])
        maxvals2[i] = np.max(images[1])
        lcd.set_cursor(1,1)
        lcd.message(str(i))
    
    mean = np.mean(maxvals-maxvals2)
    rms = np.sqrt(np.mean((maxvals-maxvals2)**2))
    std1 = np.std(maxvals)
    std2 = np.std(maxvals2)
    
    return mean,rms,std1,std2,maxvals,maxvals2
  
  
def init(leds,interface=True):
            
    #SETUP LEDS
    #13 Blue, 19 = UV, 26 = Red 
    #leds = [26,19,13]
    gpio.setmode(gpio.BCM)
    
    for i in leds:
        gpio.setup(i,gpio.OUT)
        gpio.output(i,gpio.LOW)
    
    #SETUP START BUTTON
    gpio.setup(6, gpio.IN, pull_up_down=gpio.PUD_UP)
    
    
    #SETUP CAMERA
    available_cameras = pyl.factory.find_devices()
    cam = pyl.factory.create_device(available_cameras[0])
    cam.open()
    cam.properties['ExposureAuto'] = 'Off'
    cam.properties['GainAuto'] = 'Off'
    cam.properties['OverlapMode'] = 'Off'
    cam.properties['Gain'] = 0
    cam.properties['PixelFormat'] = 'Mono12'
    
    if interface:
        # Raspberry Pi pin configuration:
        lcd_rs        = 27
        lcd_en        = 22
        lcd_d4        = 25
        lcd_d5        = 24
        lcd_d6        = 23
        lcd_d7        = 18
        lcd_backlight = 4
        
        
        #Rows and columns
        lcd_columns = 16
        lcd_rows    = 2
        lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                                   lcd_columns, lcd_rows, lcd_backlight)
                                   
        A_PIN  = 7
        B_PIN  = 9
    
        encoder = gaugette.rotary_encoder.RotaryEncoder(A_PIN, B_PIN)
        
        return cam,lcd,encoder
    return cam


def takePics(cam,leds,exp=[1500,1500],masks=None):
    images = []
    for i in leds:
        images.append(acquire(cam,exp[leds.index(i)],i))  
    if masks==None:
        return images
    images[0] = images[0]*masks[0]
    images[1] = images[1]*masks[1]
    return images
    
def normalize_exposure(images,variance=10):
    exposures=np.empty(2,float)
    intensities=np.empty(2,int)
    for i in range(len(images)):
        image = gaussian_filter(images[i],variance).astype(float)
        intensity = np.max(image)
        intensities[i] = intensity
        
    exposures[0] = 1.
    exposures[1] = intensities[0]/intensities[1]
        
    return exposures
    
def spatial_normalize(cam,leds,initial_exposure=[500,500]):

    images = takePics(cam,leds,exp=initial_exposure)
    ratios = normalize_exposure(images)
    new_exp = np.asarray(initial_exposure,int)*ratios
    images2 = takePics(cam,leds,new_exp)
    
    intensity_masks = np.ones_like(images2,dtype=float)    
    for i in range(len(images2)):
        smooth = gaussian_filter(images2[i],10).astype(float)
        max_intensity = np.max(smooth)
        good_area = smooth>50
        intensity_masks[i][good_area] = max_intensity/smooth[good_area]
    return ratios,intensity_masks        
    
# Raspberry Pi pin configuration:
lcd_rs        = 27
lcd_en        = 22
lcd_d4        = 25
lcd_d5        = 24
lcd_d6        = 23
lcd_d7        = 18
lcd_backlight = 4


#Rows and columns
lcd_columns = 16
lcd_rows    = 2
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)
    

    
if __name__ == '__main__':
    
    leds=[19,13]
    cam = init(leds)
    initial_exposure=[1500,1500]
    trials = 100
    

    images = takePics(cam,leds,initial_exposure)
    exposures = normalize(images,initial_exposure[0],4)
    mean,meansq,std1,std2,mv1,mv2 = calcVar(cam,exposures,trials)
    print('Mean: {}, Mean Squared: {}, STD1: {}, STD2: {}'.format(mean,meansq,std1,std2))
    plt.figure()
    plt.plot(mv1,'r',label='UV')
    plt.plot(mv2,'b',label='Blue')
    plt.legend()
    plt.ylim([0,4095])
        
    
  