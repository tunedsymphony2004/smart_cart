#importing the libraries
import I2C_LCD_driver
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep

#Setting up the LCD display
lcd = I2C_LCD_driver.lcd()

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

# Function to read RFID tag and return its ID
def read_rfid():
    rfid = ""
    while True:
        data = read.read()[1] #Read byte from serial port
        if data == b'\x02': #Check for start byte
            for i in range(12): #Read 12 bytes and store it in rfid
                data = read.read()[1]
                rfid += data.decode("utf-8")
            break #Break out of the loop
    return rfid #Return rfid


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


#initial display screen
lcd.lcd_display_string("WELCOME TO SMART",1,0)
lcd.lcd_display_string("SHOPPING CART",2,0)
sleep(2)

#main loop
while True:
    lcd.lcd_clear()
    lcd.lcd_display_string("PLACE YOUR ITEMS",1,1)
    rfid=read_rfid()
    product_name, product_price= get_product(rfid)
    if product_name!="Unknown":
        cart.append(product_name)
        total+=product_price
        lcd.lcd_display_string("Item: {}".format(product_name), 1,0)
        lcd.lcd_display_string("Price: {}".format(product_price), 2,0)
        time.sleep(2)
        lcd.lcd_display_string("Total: {}".format(total), 1,0)
        lcd.lcd_display_string("Items: {}".format(len(cart)), 2,0)

    else:

        lcd.lcd_display_string("INVALID PRODUCT",1,O)
        time.sleep(2)
        lcd.lcd_clear()
