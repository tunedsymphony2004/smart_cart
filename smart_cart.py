#import libraries
import I2C_LCD_driver
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import sqlite3

# Setting up the LCD display
lcd = I2C_LCD_driver.lcd()


# Setting up the RFID reader
read = SimpleMFRC522()

# Setting up the database connection
conn = sqlite3.connect('products.db')
c = conn.cursor()

# Creating a table for products if not exists
c.execute('''CREATE TABLE IF NOT EXISTS products
             (rfid text, name text, price real)''')

# Inserting some sample products into the table
c.execute("INSERT INTO products VALUES ('577909759756', 'Milk', 40)")
c.execute("INSERT INTO products VALUES ('808564968078', 'Eggs', 10)")
c.execute("INSERT INTO products VALUES ('345678901234', 'Bread', 50)")
conn.commit()

# Initializing the cart list and total amount
cart = []
total = 0

# Defining a function to display the cart items and total on LCD
def display_cart():
    global cart, total
    lcd.lcd_clear()
    lcd.lcd_display_string("Cart items: " + str(len(cart)),1,0)
    lcd.lcd_display_string("Total: ₹" + str(total),2,0)

# Defining a function to add an item to the cart
def add_item(rfid):
    global cart, total
    # Querying the database for the product details
    c.execute("SELECT name, price FROM products WHERE rfid = ?", (rfid,))
    result = c.fetchone()
    if result:
        # If the product is found, append it to the cart and update the total
        name, price = result
        cart.append((name, price))
        total += price
        # Display a message on LCD
        lcd.lcd_clear()
        lcd.lcd_display_string(("Added " + name),1,0)
        lcd.lcd_display_string("Price: ₹" + str(price),2,0)
        time.sleep(2)
        display_cart()
    else:
        # If the product is not found, display an error message on LCD
        lcd.lcd_clear()
        lcd.lcd_display_string(("Product not found"),1,0)
        time.sleep(2)
        display_cart()

# Defining a function to remove an item from the cart
def remove_item(rfid):
    global cart, total
    # Searching the cart for the product details
    for item in cart:
        if item[0] == rfid:
            # If the product is found, remove it from the cart and update the total
            name, price = item
            cart.remove(item)
            total -= price
            # Display a message on LCD
            lcd.lcd_clear()
            lcd.lcd_display_string(("Removed " + name),1,0)
            lcd.lcd_display_string(("Price: ₹" + str(price)),2,0)
            time.sleep(2)
            display_cart()
            break
    else:
        # If the product is not found, display an error message on LCD
        lcd.lcd_clear()
        lcd.lcd_display_string(("Product not in cart"),1,0)
        time.sleep(2)
        display_cart()

# Defining a function to clear the cart and reset the total
def clear_cart():
    global cart, total
    cart = []
    total = 0
    # Display a message on LCD
    lcd.lcd_clear()
    lcd.lcd_display_string(("Cart cleared"),1,0)
    time.sleep(2)
    display_cart()

# Displaying the initial message on LCD
lcd.lcd_clear()
lcd.lcd_display_string(("Welcome to Smart"),1,0)
lcd.lcd_display_string(("Shopping Cart"),2,0)
time.sleep(2)
display_cart()

# Setting up a button to clear the cart
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Main loop to read RFID tags and button press
while True:
    # Reading data from RFID reader
    data = read.read()[1]
    if data:
        # Checking if the RFID tag is already in the cart or not
        if data in [item[0] for item in cart]:
            # If yes, remove it from the cart
            remove_item(data)
        else:
            print("If no, add it to the cart")