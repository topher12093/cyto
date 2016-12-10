import gaugette.rotary_encoder
import Adafruit_CharLCD as LCD

"""
LCD Functionality

-Define pins
-Creates the lcd object

"""


class Lcd:

	#Pin Configurations on the Raspberry Pi

	lcd_rs = 27
	lcd_en = 22
	lcd_d4 = 25
	lcd_d5 = 24
	lcd_d6 = 23
	lcd_d7 = 18
	lcd_backlight = 4

	lcd_columns = 16
	lcd_rows  = 2
    
    #Pins for Encoder
    
	a_pin = 7
	b_pin = 9

	def __init__(self):

		#Setup the LCD screen and encoder
		self.setup = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                                   lcd_columns, lcd_rows, lcd_backlight)
		self.encoder_setup = gaugette.rotary_encoder.RotaryEncoder(a_pin, b_pin)



	#Need to add functionality for common displays (i.e "Home screen" that is displaying properties)
	#we could
