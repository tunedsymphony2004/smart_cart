#importing the libraries
import I2C_LCD_driver
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

#Setting up the LCD display
lcd = I2C_LCD_driver.lcd()

# Setting up the RFID reader
read = SimpleMFRC522()

# Setting up the button
button = 10 #GPIO pin number
GPIO.setmode(GPIO.BOARD) #BOARD is for physical pins
GPIO.setwarnings(False)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# Defining a function to display the cart items and total on LCD
def display_cart():
    global cart, total
    # Displaying the initial message on LCD
    lcd.lcd_clear()
    lcd.lcd_display_string(("Welcome to Smart"),1,0)
    lcd.lcd_display_string(("Shopping Cart"),2,0)
    time.sleep(2)
    lcd.lcd_clear()
    lcd.lcd_display_string(("Cart items: " + str(len(cart))),1,0)
    lcd.lcd_display_string(("Total: $" + str(total)),2,0)


# Initializing the cart variables
cart = [] #List of items in the cart
total = 0 #Total value of the cart

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

# Main loop
while True:

    display_cart()
    
    # Check if button is pressed
    if GPIO.input(button) == GPIO.LOW:
        
        # Read RFID tag ID
        rfid = read_rfid()
        
        # Get product details from RFID tag ID
        product_name, product_price = get_product(rfid)
        
        # Check if product is valid
        if product_name != "Unknown":
            
            # Add product to cart list and update total value
            cart.append(product_name)
            total += product_price
            
            # Display product details and total value on LCD
            lcd.lcd_display_string("Item: {}".format(product_name), 1,0)
            lcd.lcd_display_string("Price: {}".format(product_price), 2,0)
            time.sleep(2)
            lcd.lcd_display_string("Total: {}".format(total), 1,0)
            lcd.lcd_display_string("Items: {}".format(len(cart)), 2,0)
            
           
        else:
            
            # Display invalid product message on LCD
            lcd.lcd_display_string("Invalid Product", 1,0)
            time.sleep(2)
            lcd.lcd_clear()


#initial display screen
#lcd.lcd_display_string("WELCOME TO SMART",1,0)
#lcd.lcd_display_string("SHOPPING CART",2,0)
#sleep(0.3)

#main loop
#while True:
    #lcd.lcd_clear()
    #lcd.lcd_display_string("PLACE YOUR ITEMS",1,1)
    #read_rfid()
