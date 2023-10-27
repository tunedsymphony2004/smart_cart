#importing the libraries
import I2C_LCD_driver
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep
import json


#Setting up the LCD display
#lcd = I2C_LCD_driver.lcd()

# Setting up the RFID reader
read = SimpleMFRC522()

# Setting up the button
button = 15 #GPIO pin number
GPIO.setmode(GPIO.BOARD) #BOARD is for physical pins
GPIO.setwarnings(False) 
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# Initializing the cart variables
cart_items = [] #List of items in the cart
cart_total = 0 #Total value of the cart

# Function to get product details from RFID tag ID
def get_product(rfid):
    product_name = ""
    product_price = 0
    
    # You can add more products here with their RFID tag IDs and prices
    if rfid == "577909759756":
        product_name = "Milk"
        product_price = 50
        
    elif rfid == "808564968078":
        product_name = "Bread"
        product_price = 40
        
    else:
        product_name = "Unknown"
        product_price = 0
        
    return (product_name, product_price) #Return a tuple of product name and price

# Function to read RFID tag and return its ID
def read_rfid():
        print("test1")
        #data = read.read()
        data = 54123654566, 54645
        data=str(data)
        print("test2")
        if data in rfid_id: 
            print("product is available",1,0)
        return rfid_id #Return rfid



#initial display screen
#lcd.lcd_display_string("WELCOME TO SMART",1,0)
#lcd.lcd_display_string("SHOPPING CART",2,0)
sleep(2)

#main loop
while True:
#    lcd.lcd_clear()
#    lcd.lcd_display_string("PLACE YOUR ITEMS",1,1)
    rfid=read_rfid()[0]
    product_name, product_price= get_product(rfid)
    if product_name!="Unknown":
        cart.append(product_name)
        total+=product_price
#        lcd.lcd_display_string("Item: {}".format(product_name), 1,0)
#        lcd.lcd_display_string("Price: {}".format(product_price), 2,0)
        time.sleep(2)
#        lcd.lcd_display_string("Total: {}".format(total), 1,0)
#        lcd.lcd_display_string("Items: {}".format(len(cart)), 2,0)

    else:

#        lcd.lcd_display_string("INVALID PRODUCT",1,O)
        time.sleep(2)
#        lcd.lcd_clear()


