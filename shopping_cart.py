
#code adapted from in-class shopping_cart.py

#worked with Krish Sarawgi 

import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import gspread
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()


products = [
    {"id":1, "name": "Chocolate Sandwich Cookies", "department": "snacks", "aisle": "cookies cakes", "price": 3.50},
    {"id":2, "name": "All-Seasons Salt", "department": "pantry", "aisle": "spices seasonings", "price": 4.99},
    {"id":3, "name": "Robust Golden Unsweetened Oolong Tea", "department": "beverages", "aisle": "tea", "price": 2.49},
    {"id":4, "name": "Smart Ones Classic Favorites Mini Rigatoni With Vodka Cream Sauce", "department": "frozen", "aisle": "frozen meals", "price": 6.99},
    {"id":5, "name": "Green Chile Anytime Sauce", "department": "pantry", "aisle": "marinades meat preparation", "price": 7.99},
    {"id":6, "name": "Dry Nose Oil", "department": "personal care", "aisle": "cold flu allergy", "price": 21.99},
    {"id":7, "name": "Pure Coconut Water With Orange", "department": "beverages", "aisle": "juice nectars", "price": 3.50},
    {"id":8, "name": "Cut Russet Potatoes Steam N' Mash", "department": "frozen", "aisle": "frozen produce", "price": 4.25},
    {"id":9, "name": "Light Strawberry Blueberry Yogurt", "department": "dairy eggs", "aisle": "yogurt", "price": 6.50},
    {"id":10, "name": "Sparkling Orange Juice & Prickly Pear Beverage", "department": "beverages", "aisle": "water seltzer sparkling water", "price": 2.99},
    {"id":11, "name": "Peach Mango Juice", "department": "beverages", "aisle": "refrigerated", "price": 1.99},
    {"id":12, "name": "Chocolate Fudge Layer Cake", "department": "frozen", "aisle": "frozen dessert", "price": 18.50},
    {"id":13, "name": "Saline Nasal Mist", "department": "personal care", "aisle": "cold flu allergy", "price": 16.00},
    {"id":14, "name": "Fresh Scent Dishwasher Cleaner", "department": "household", "aisle": "dish detergents", "price": 4.99},
    {"id":15, "name": "Overnight Diapers Size 6", "department": "babies", "aisle": "diapers wipes", "price": 25.50},
    {"id":16, "name": "Mint Chocolate Flavored Syrup", "department": "snacks", "aisle": "ice cream toppings", "price": 4.50},
    {"id":17, "name": "Rendered Duck Fat", "department": "meat seafood", "aisle": "poultry counter", "price": 9.99},
    {"id":18, "name": "Pizza for One Suprema Frozen Pizza", "department": "frozen", "aisle": "frozen pizza", "price": 12.50},
    {"id":19, "name": "Gluten Free Quinoa Three Cheese & Mushroom Blend", "department": "dry goods pasta", "aisle": "grains rice dried goods", "price": 3.99},
    {"id":20, "name": "Pomegranate Cranberry & Aloe Vera Enrich Drink", "department": "beverages", "aisle": "juice nectars", "price": 4.25}
] # based on data from Instacart: https://www.instacart.com/datasets/grocery-shopping-2017



#googlesheets_products = []
#
#DOCUMENT_ID = os.getenv("GOOGLE_SHEET_ID", default="OOPS")
#SHEET_NAME = os.getenv("SHEET_NAME", default="Products-2021")
#
#CREDENTIALS_FILEPATH = os.path.join(os.path.dirname(__file__), "auth", "google-credentials.json")
#
#AUTH_SCOPE = [
#    "https://www.googleapis.com/auth/spreadsheets", #> Allows read/write access to the user's sheets and their properties.
#    "https://www.googleapis.com/auth/drive.file" #> Per-file access to files created or opened by the app.
#]
#
#credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILEPATH, AUTH_SCOPE)
#print("CREDS:", type(credentials)) #> <class 'oauth2client.service_account.ServiceAccountCredentials'>
#
#client = gspread.authorize(credentials)
#print("CLIENT:", type(client)) #> <class 'gspread.client.Client'>
#
#print("-----------------")
#print("READING DOCUMENT...")
#
## access the document:
#doc = client.open_by_key(DOCUMENT_ID)
#print("DOC:", type(doc), doc.title) #> <class 'gspread.models.Spreadsheet'>
# 
## access a sheet within the document:
#sheet = doc.worksheet(SHEET_NAME)
#print("SHEET:", type(sheet), sheet.title)#> <class 'gspread.models.Worksheet'>
#
## fetch all data from that sheet:
#rows = sheet.get_all_records()
#print("ROWS:", type(rows)) #> <class 'list'>
#
## loop through and print each row, one at a time:
#for row in rows:
#    googlesheets_products.append(row)


def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    Param: my_price (int or float) like 4000.444444
    Example: to_usd(4000.444444)
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71

print("Hi! Please select the items you've scanned to generate a receipt. When you've finished, type 'done'. ")

print("---------------------------------")

total_price = 0 
selected_ids = []
valid_ids = []

for product in products:
    valid_ids.append(str(product["id"]))

while True:
    selected_id = input("Please input a product identifier: ")

    if selected_id.lower() == "done":
        break
    elif selected_id in valid_ids:
        selected_ids.append(selected_id)
    else: 
        print("Make sure you input a valid product identifier! Please try again.")

print("> ---------------------------------")
print("> NICK'S GROCERY")
print("> WWW.NICKSGROCERY.COM")
print("> ---------------------------------")

#https://www.programiz.com/python-programming/datetime/current-datetime
from datetime import datetime
now = datetime.now()

date_time = now.strftime("%Y-%m-%d %H:%M %p")

print("> CHECKOUT AT: " + date_time)
print("> ---------------------------------")
print("> SELECTED PRODUCTS:")

for selected_id in selected_ids:
        matching_products = [p for p in products if str(p["id"]) == str(selected_id)]
        matching_product = matching_products[0]
        total_price = total_price + matching_product["price"]
        print("... " + matching_product["name"] + " " + "(" + str(to_usd(matching_product["price"]) + ")"))

tax_rate = float(os.getenv("TAX_RATE", default="0.0875"))
tax = total_price * tax_rate
print("> SUBTOTAL: " + str(to_usd(total_price)))
print("> TAX: " + str(to_usd(tax)))
print("> TOTAL: " + str(to_usd(tax + total_price)))
print("> ---------------------------------")
print("> THANKS, SEE YOU AGAIN SOON!")
print("> ---------------------------------")


#email

#email_choice = input("Do you want your receipt to be emailed to you? Please indicate 'yes' or 'no': ")
#email_choice.lower()
#
#if email_choice == "yes": 
#    user_email = input("Please type the customer's email address: ")
#    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", default="OPPS, please set env var called 'SENDGRID_API_KEY'")
#    SENDER_ADDRESS = os.getenv("SENDER_ADDRESS", default="OOPS, please set env var called 'SENDER_ADDRESS'")
#
#    client = SendGridAPIClient(SENDGRID_API_KEY)
#
#    subject = "Your Receipt from the Green Grocery Store"
#
#    html_content = ""
#
#    html_content += "---------------------------------<br>"
#
#    for selected_id in selected_ids:
#        matching_products = [p for p in googlesheets_products if str(p["id"]) == str(selected_id)]
#        matching_product = matching_products[0]
#        html_content += " ... " + matching_product["name"] + " (" + to_usd(matching_product["price"]) + ")<br>"
#
#    html_content += "---------------------------------<br>"
#
#    message = Mail(
#        from_email=SENDER_ADDRESS,
#        to_emails=user_email,
#        subject=subject,
#        html_content=html_content)
#    
#    try:
#        response = client.send(message)
#        if str(response.status.code) == "202":
#            print("Email to", user_email, "has been sent.")
#    
#    except Exception as err: 
#        print(type(err))
#        print(err)
#    
#    print("")