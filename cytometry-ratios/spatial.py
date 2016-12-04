import matplotlib.pyplot as plt
from NormalizeData import *

if __name__ == '__main__':
    leds=[19,13]
    cam = init(leds,False)
    initial_exposures = np.array([8000,8000],int)
    """    
    images = takePics(cam,leds,initial_exposures)
    plt.subplot(121)
    plt.imshow(images[0],vmin=0,vmax=4095)
    plt.subplot(122)
    plt.imshow(images[1],vmin=0,vmax=4095)
    
    ratios,masks = spatial_normalize(cam,leds,initial_exposures)
    
    np.save('ratios',ratios)
    np.save('masks',masks)
    
    new_exp = ratios*initial_exposures
    images2 = takePics(cam,leds,new_exp,masks)
    
    plt.figure()
    plt.subplot(121)
    plt.imshow(images2[0],vmin=0,vmax=4095)
    plt.subplot(122)
    plt.imshow(images2[1],vmin=0,vmax=4095)
    """
    ratios = np.load('ratios.npy')
    masks = np.load('masks.npy')
    
    exposures = ratios*initial_exposures
    
    images = takePics(cam,leds,exposures,masks)
    
    plt.subplot(121)
    plt.imshow(images[0],'gray',vmin=0,vmax=4095)
    plt.subplot(122)
    plt.imshow(images[1],'gray',vmin=0,vmax=4095)
        
    cam.close()