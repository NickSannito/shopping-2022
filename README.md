# shopping-2022

## Setup 

Create a virtual environment: 

```sh
conda create -n shopping-2022 python=3.8
```

Activate the virtual environment: 

```sh
conda activate shopping-2022
```

Install package dependencies: 

```sh
pip install -r requirements.txt
```

## Usage 

Run the shopping cart app: 

```sh
python shopping_cart.py
```

## General App Usage: 

- Type product identifiers for each item in the shopping cart. 

- If a valid product identifier is not typed, you will be notified and the products can be input again.

- Once all of the items in the cart have been entered, type 'done' (the app should be able to handle any pattern of caps/lowercase letters)

- Based on the inputed product identifiers, a receipt including the selected products, their prices, the product subtotal, taxes, and the total price will be generated. 


## Configuring Tax Rate 

This app allows you to configure a custom tax rate. To do this, follow the steps below: 

- Create a file ending in '.env' that contains your desired tax rate. If your desired tax rate were 7.5%, for example, format it as follows:

```sh
TAX_RATE = 0.075
```

- Your tax rate can be any decimal between 0 and 1

- Place your '.env' file in this directory with the rest of the shopping-2022 associated files

- If no custom tax rate is entered, a rate of 8.75 will be used as default 
