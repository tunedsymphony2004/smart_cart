#importing the libraries
import I2C_LCD_driver
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

#Setting up the LCD display
lcd = I2C_LCD_driver.lcd()

# Setting up the RFID reader
read = SimpleMFRC522()

items={"808564968078":["Bread", 50],
"145650306283": ["Milk", 30],
"577909759756": ["Egg", 10],
"220501638258": ["Coke", 20]}

item_list=[["Bread",50],["Milk",30],["Egg",10],["Coke",20]]

#Include the buzzer pin
buzzer = 40


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(buzzer,GPIO.OUT)

def rfid_read():
    read = SimpleMFRC522()
    GPIO.setup(buzzer, GPIO.OUT)
    data=read.read()
    GPIO.output(buzzer,GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(buzzer,GPIO.LOW)
    print(data)
    return data

def cartlen(cart):
    count=list(cart.values())
    return sum(count)


def sms():
    from twilio.rest import Client
    itemno = str(cartlen(cart))
    cost = str(cart_sum(cart, item_list))
    account_sid = 'AC99a81d21e965ed6872119b5f622fa915'
    auth_token = 'f560c0603a3f921d3b3913e9460ab201'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    from_='+14179003883',
    body= f' Number of items bought : '+itemno+' \nTotal Bill Amount : '+cost+  '\nYour total bill amount can be paid to  http://surl.li/iltfd\n\nHave a nice day...  \nTanvi ki Tapri',
    to='+91'+str(input("ENTER YOUR PHONE NUMBER: "))
    )
    print(message.sid)




def cart_sum(cart,item_list):
    sum=0
    for i in item_list:
        sum+= cart[i[0]] * i[1]
    return sum

def show(cart, item_list):
    from prettytable import PrettyTable
    MyTable=PrettyTable(["ITEM NAME", "ITEM PRICE", "ITEM QUANTITY", "TOTAL"])
    for i in range(len(item_list)):
        item=item_list[i]
        quantity=cart[item[0]]
        price=item[1]
        MyTable.add_row([item[0], price, quantity, price*quantity])
    MyTable.add_row(["","","NET TOTAL:", cart_sum(cart, item_list)])
    print(MyTable)
    

#initial display screen
lcd.lcd_display_string("WELCOME TO SMART",1,0)
lcd.lcd_display_string("SHOPPING CART",2,0)
time.sleep(5)

cart={"Bread":0, "Milk":0, "Egg":0, "Coke":0}
while True:
    lcd.lcd_clear()
    lcd.lcd_display_string("PLACE YOUR ITEMS",1,1)
    id=str(rfid_read()[0])
    lcd.lcd_clear()
    value=items[id] #to access value from dictionary
    lcd.lcd_display_string("Name:"+str(value[0]),1,0)
    lcd.lcd_display_string("Price:"+str(value[1]),2,0)
    time.sleep(2)
    print("""MAKE CHOICE\n1. ADD ITEM\n2. REMOVE ITEM\n3.SHOW FINAL PRICE""")
    lcd.lcd_display_string("MAKE CHOICE",1,0)
    time.sleep(1)
    lcd.lcd_display_string("1.ADD ITEMS",1,0)
    lcd.lcd_display_string("2.REMOVE ITEMS",2,0)
    choice=int(input())
    item_name=value[0]
    quantity=cart[item_name]
    if choice==1:
        cart.update({item_name:quantity+1})
    elif choice==2:
        cart.update({item_name:quantity-1})
    elif choice==3:
        show(cart,item_list)
        sms()
    else:
        print("INVALID FUNCTION")

    number_of_items=str(cartlen(cart))
    total_price=str(cart_sum(cart,item_list))
    lcd.lcd_display_string("Total items:"+number_of_items,1,0)
    lcd.lcd_display_string("Total price:"+total_price,2,0)
    time.sleep(2)
    GPIO.cleanup()
