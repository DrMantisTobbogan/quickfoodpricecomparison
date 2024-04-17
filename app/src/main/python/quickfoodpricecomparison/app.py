"""
This application helps quickly convert between food prices per a unit of mass or volume for metric and imperial systems.
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from toga.platform import current_platform
# from typing import Bytes
from pint import UnitRegistry
from pathlib import Path
import pickle
import time
import os


# To use default settings, set locale to None or leave the second argument blank.
formal_name = "Quick Food Price Comparison"
full_name = "com.drmantistobbogan.foodpricecomparison"
ureg = UnitRegistry()
selection_list = [{'name': 'Price per kilogram', 'mass': ureg.kilogram * 1},
                  {'name': 'Price per 900 grams', 'mass': ureg.gram * 900},
                  {'name': 'Price per 800 grams', 'mass': ureg.gram * 800},
                  {'name': 'Price per 750 grams', 'mass': ureg.gram * 750},
                  {'name': 'Price per 700 grams', 'mass': ureg.gram * 700},
                  {'name': 'Price per 600 grams', 'mass': ureg.gram * 600},
                  {'name': 'Price per 500 grams', 'mass': ureg.gram * 500},
                  {'name': 'Price per 400 grams', 'mass': ureg.gram * 400},
                  {'name': 'Price per 250 grams', 'mass': ureg.gram * 250},
                  {'name': 'Price per 200 grams', 'mass': ureg.gram * 200},
                  {'name': 'Price per 100 grams', 'mass': ureg.gram * 100},
                  {'name': 'Price per gram', 'mass': ureg.gram * 1},
                  {'name': 'Price per milligram', 'mass': ureg.milligram * 1},
                  {'name': 'Price per pound', 'mass': ureg.pound * 1},
                  {'name': 'Price per 12 oz', 'mass': ureg.ounce * 12},
                  {'name': 'Price per 8 oz', 'mass': ureg.ounce * 8},
                  {'name': 'Price per 6 oz', 'mass': ureg.ounce * 6},
                  {'name': 'Price per 4 oz', 'mass': ureg.ounce * 4},
                  {'name': 'Price per 2 oz', 'mass': ureg.ounce * 2},
                  {'name': 'Price per oz', 'mass': ureg.ounce * 1}]

text_style = Pack(padding=(0, 5), font_size=14)
button_style = Pack(padding=(0, 5), font_size=14, flex=150)


def read_food_density() -> list:
    '''
    Toga won't pass the file in.
    # Specify the path to your CSV file
    csv_file_path = r"D:\python_workspace\quickfoodpricecomparison\src\quickfoodpricecomparison\resources\food_density.csv"
    csv_data = []

    # Open the CSV file and read its contents
    with open(csv_file_path, "r", encoding='utf-8-sig') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            csv_data.append(row)
    '''
    csv_data = [{'food_name': 'alcohol, ethyl', 'g_ml': '0.789', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Beverages, alcoholic'}, {'food_name': 'alfalfa, leaf, meal', 'g_ml': '0.23', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Vegetables'}, {'food_name': 'alfalfa, meal, dehydrated 17%', 'g_ml': '0.32', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Vegetables'}, {'food_name': 'alfalfa, meal, fine ground', 'g_ml': '0.295', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Vegetables'}, {'food_name': 'alfalfa, meal, suncured 13%', 'g_ml': '0.22', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Vegetables'}, {'food_name': 'alfalfa, seed', 'g_ml': '0.745', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Vegetables'}, {'food_name': 'alfalfa, stem meal', 'g_ml': '0.19', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Vegetables'}, {'food_name': 'alfalfa,meal, dehydrated 13%', 'g_ml': '0.275', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Vegetables'}, {'food_name': 'almonds', 'g_ml': '0.46', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Nuts and seeds'}, {'food_name': 'animal fat', 'g_ml': '0.7', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Oils and fats'}, {'food_name': 'apple juice, canned or bottled, unsweetened, with added ascorbic acid', 'g_ml': '1.043396693', 'specific_gravity': '1.045725', 'biblio_id': 'USDA', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'apple juice, canned or bottled, unsweetened, without added ascorbic acid', 'g_ml': '1.043396693', 'specific_gravity': '1.045725', 'biblio_id': 'USDA', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'apple slices, dried', 'g_ml': '0.24', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Fruits'}, {'food_name': 'arrowroot/cocoyam, boiled', 'g_ml': '0.535', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Tubers and products'}, {'food_name': 'arrowroot/cocoyam, raw', 'g_ml': '0.519999981', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Tubers and products'}, {'food_name': 'baking powder', 'g_ml': '0.9', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Miscellaneous foods'}, {'food_name': 'barley', 'g_ml': '0.62', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Cereal and cereal products'}, {'food_name': 'barley malt, flour', 'g_ml': '0.72', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'barley, fine ground', 'g_ml': '0.74', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'barley, flour', 'g_ml': '0.61', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'barley, flour, malted ', 'g_ml': '0.64', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'barley, ground', 'g_ml': '0.4', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'barley, malted', 'g_ml': '0.49', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'barley, meal', 'g_ml': '0.45', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'barley, rolled', 'g_ml': '0.36', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'barley, scoured', 'g_ml': '0.66', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'barley, whole', 'g_ml': '0.65', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'bean soup', 'g_ml': '1.054', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Soups'}, {'food_name': 'beans, white', 'g_ml': '0.73', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Legumes'}, {'food_name': 'beef and noodles (no sauce)', 'g_ml': '0.65', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Mixed dishes'}, {'food_name': 'beef and noodles in gravy (mixture)', 'g_ml': '1.038', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Mixed dishes'}, {'food_name': 'beef stew, canned', 'g_ml': '1.05', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Mixed dishes'}, {'food_name': 'beef, noodles and vegetables (no sauce)', 'g_ml': '0.675', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Mixed dishes'}, {'food_name': 'beer, commercial (white cap etc.)', 'g_ml': '0.970000029', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Beverages, alcoholic'}, {'food_name': 'beer, light', 'g_ml': '1.00024284', 'specific_gravity': '1.00247485', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'beer, light, bud light', 'g_ml': '1.000467488', 'specific_gravity': '1.0027', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'beer, light, budweiser select', 'g_ml': '0.996875504', 'specific_gravity': '0.9991', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'beer, light, michelob ultra', 'g_ml': '0.99587773', 'specific_gravity': '0.9981', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'beer, local (non specific)', 'g_ml': '0.959999979', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Beverages, alcoholic'}, {'food_name': 'beer, pilsner', 'g_ml': '1.007', 'specific_gravity': '', 'biblio_id': 'DK', 'category': 'Beverages, alcoholic'}, {'food_name': 'beer, pilsner, 4\xa0°c', 'g_ml': '1.008', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Beverages, alcoholic'}, {'food_name': 'beer, regular, all', 'g_ml': '1.008040386', 'specific_gravity': '1.010289796', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'beer, regular, budweiser', 'g_ml': '1.004757915', 'specific_gravity': '1.007', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'beverages, fruit juice drink, reduced sugar, with vitamin e added', 'g_ml': '1.043097361', 'specific_gravity': '1.045425', 'biblio_id': 'USDA', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'biscuits', 'g_ml': '0.47', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Cereal and cereal products'}, {'food_name': 'blood, flour', 'g_ml': '0.48', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Meat and meat products'}, {'food_name': 'blood, meal', 'g_ml': '0.62', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Meat and meat products'}, {'food_name': 'bone and meat meal, loose', 'g_ml': '0.72', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Meat and meat products'}, {'food_name': 'bone meal, loose', 'g_ml': '0.88', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Meat and meat products'}, {'food_name': 'bran', 'g_ml': '0.56', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'bread', 'g_ml': '0.29', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Cereal and cereal products'}, {'food_name': 'bread, cornbread ', 'g_ml': '0.433', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Cereal and cereal products'}, {'food_name': 'bread, roll, soft', 'g_ml': '0.18', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Cereal and cereal products'}, {'food_name': 'bread, white', 'g_ml': '0.42', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Cereal and cereal products'}, {'food_name': 'bread, white, sliced, prepacked', 'g_ml': '0.29', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Cereal and cereal products'}, {'food_name': 'breadcrumbs', 'g_ml': '0.45', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Cereal and cereal products'}, {'food_name': 'breakfast cereal, cornflakes (dry cereal) ', 'g_ml': '0.117', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Cereal and cereal products'}, {'food_name': 'breakfast cereal, muesli w/ fruits&nuts', 'g_ml': '0.37', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Cereal and cereal products'}, {'food_name': 'breakfast cereal, raisin bran', 'g_ml': '0.26', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Cereal and cereal products'}, {'food_name': 'breakfast cereal, type cheerios', 'g_ml': '0.13', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Cereal and cereal products'}, {'food_name': 'breakfast cereal, type corn flakes', 'g_ml': '0.1', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Cereal and cereal products'}, {'food_name': 'breakfast cereal, type crispix', 'g_ml': '0.13', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Cereal and cereal products'}, {'food_name': 'breakfast cereal, type frosted flakes', 'g_ml': '0.18', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Cereal and cereal products'}, {'food_name': 'breakfast cereal, type just right', 'g_ml': '0.24', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Cereal and cereal products'}, {'food_name': 'breakfast cereal, type rice krispies', 'g_ml': '0.12', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Cereal and cereal products'}, {'food_name': 'broccoli casserole', 'g_ml': '0.95', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Mixed dishes'}, {'food_name': 'buckwheat, bran', 'g_ml': '0.25', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'buckwheat, flour', 'g_ml': '0.66', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'buckwheat, whole', 'g_ml': '0.625', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'bulrush mille, fermented flour', 'g_ml': '0.56', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Cereal and cereal products'}, {'food_name': 'butter', 'g_ml': '0.911', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Milk and dairy products'}, {'food_name': 'butter, margarine', 'g_ml': '0.96', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Milk and dairy products'}, {'food_name': 'buttermilk, dried', 'g_ml': '0.5', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Milk and dairy products'}, {'food_name': 'cake ', 'g_ml': '0.415', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Cereal and cereal products'}, {'food_name': 'cake mix', 'g_ml': '0.7', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'carbonated beverage, tonic water', 'g_ml': '1.021054882', 'specific_gravity': '1.023333333', 'biblio_id': 'USDA', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'carrot, raw, chopped', 'g_ml': '0.54', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Vegetables'}, {'food_name': 'carrot, raw, grated', 'g_ml': '0.71', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Vegetables'}, {'food_name': 'casein', 'g_ml': '0.58', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Milk and dairy products'}, {'food_name': 'cashews', 'g_ml': '0.5', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Nuts and seeds'}, {'food_name': 'cassava, boiled', 'g_ml': '0.63', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Tubers and products'}, {'food_name': 'cassava, raw', 'g_ml': '0.629999995', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Tubers and products'}, {'food_name': 'cassava,flour', 'g_ml': '0.550000012', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Tubers and products'}, {'food_name': 'cauliflower, boiled', 'g_ml': '0.45', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Vegetables'}, {'food_name': 'cheddar cheese soup', 'g_ml': '1.046', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Soups'}, {'food_name': 'cheese tortellini', 'g_ml': '1.029', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Mixed dishes'}, {'food_name': 'cheese, emmentaler, grated', 'g_ml': '0.34', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Milk and dairy products'}, {'food_name': 'chicken and dumplings (mixture)', 'g_ml': '1.038', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Mixed dishes'}, {'food_name': 'chicken noodle soup', 'g_ml': '1', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Soups'}, {'food_name': 'chili, green', 'g_ml': '0.5', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Vegetables'}, {'food_name': 'chili, red', 'g_ml': '0.5', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Vegetables'}, {'food_name': 'cinnamon, powder', 'g_ml': '0.56', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Herbes and spices'}, {'food_name': 'clover, seed', 'g_ml': '0.77', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Herbes and spices'}, {'food_name': 'coconut chips', 'g_ml': '0.61', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Nuts and seeds'}, {'food_name': 'coffee, brewed', 'g_ml': '1', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Tea, cacao, coffee and drinking powders'}, {'food_name': 'coffee, expresso', 'g_ml': '1', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Tea, cacao, coffee and drinking powders'}, {'food_name': 'coffee, green (beans)', 'g_ml': '0.605', 'specific_gravity': '0.59-0.62', 'biblio_id': 'ASI', 'category': 'Tea, cacao, coffee and drinking powders'}, {'food_name': 'coffee, powder (nescafé)', 'g_ml': '0.25', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Tea, cacao, coffee and drinking powders'}, {'food_name': 'coffee, roasted (beans)', 'g_ml': '0.365', 'specific_gravity': '0.35-0.38', 'biblio_id': 'ASI', 'category': 'Tea, cacao, coffee and drinking powders'}, {'food_name': 'cooking oil, elianto oil, salad, golden fry, rina', 'g_ml': '0.879999995', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Oils and fats'}, {'food_name': 'cooking oil, sima', 'g_ml': '0.88', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Oils and fats'}, {'food_name': 'cooking oil, tily, chipo, pura', 'g_ml': '0.88', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Oils and fats'}, {'food_name': 'corn/maize flour, white', 'g_ml': '0.550000012', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Cereal and cereal products'}, {'food_name': 'corn/maize starch, loosely packed', 'g_ml': '0.54', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Cereal and cereal products'}, {'food_name': 'corn/maize sugar', 'g_ml': '0.33', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'corn/maize, boiled', 'g_ml': '0.899999976', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Cereal and cereal products'}, {'food_name': 'corn/maize, boiled with fat', 'g_ml': '0.899999976', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Cereal and cereal products'}, {'food_name': 'corn/maize, bran', 'g_ml': '0.21', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'corn/maize, chops (coarse)', 'g_ml': '0.67', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'corn/maize, chops (fine)', 'g_ml': '0.6', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'corn/maize, chops (medium)', 'g_ml': '0.64', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'corn/maize, cobs', 'g_ml': '0.27', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'corn/maize, cracked (coarse)', 'g_ml': '0.64', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'corn/maize, ear', 'g_ml': '0.9', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Cereal and cereal products'}, {'food_name': 'corn/maize, ear', 'g_ml': '0.9', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'corn/maize, fermented flour ', 'g_ml': '0.55', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Cereal and cereal products'}, {'food_name': 'corn/maize, flour', 'g_ml': '0.82', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'corn/maize, flour ', 'g_ml': '0.62', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'corn/maize, germ flour', 'g_ml': '0.56', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'corn/maize, gluten flour', 'g_ml': '0.6', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'corn/maize, green, sweet corn, boiled', 'g_ml': '0.73', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Vegetables'}, {'food_name': 'corn/maize, green, sweet corn, raw', 'g_ml': '0.61', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Vegetables'}, {'food_name': 'corn/maize, grits', 'g_ml': '0.665', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'corn/maize, ground', 'g_ml': '0.56', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'corn/maize, kibbled', 'g_ml': '0.335', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'corn/maize, mash', 'g_ml': '0.72', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'corn/maize, meal', 'g_ml': '0.64', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'corn/maize, shelled', 'g_ml': '0.72', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Cereal and cereal products'}, {'food_name': 'corn/maize, starch', 'g_ml': '0.67', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'corn/maize, starch, tightly packed', 'g_ml': '0.63', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Cereal and cereal products'}, {'food_name': 'corn/maize, white, boiled', 'g_ml': '0.850000024', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Cereal and cereal products'}, {'food_name': 'corn/maize, white, dry', 'g_ml': '0.810000002', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Cereal and cereal products'}, {'food_name': 'corn/maize, whole kernel, dried, cracked (njenga)', 'g_ml': '0.810000002', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Cereal and cereal products'}, {'food_name': 'corn/maize, whole kernel, dried, cracked, boiled (njenga)', 'g_ml': '1.070000052', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Cereal and cereal products'}, {'food_name': 'corn/maize, whole shelled', 'g_ml': '0.72', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'cow intestine, boiled', 'g_ml': '0.58', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Meat and meat products'}, {'food_name': 'cow, intestine, raw', 'g_ml': '0.93', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Meat and meat products'}, {'food_name': 'cow, lean, no bone, raw', 'g_ml': '0.96', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Meat and meat products'}, {'food_name': 'cowpeas', 'g_ml': '0.72', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Legumes'}, {'food_name': 'cowpeas, dried, boiled', 'g_ml': '0.75', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Legumes'}, {'food_name': 'cowpeas, dried, raw', 'g_ml': '0.959999979', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Legumes'}, {'food_name': 'cranberry juice cocktail, bottled', 'g_ml': '1.051653269', 'specific_gravity': '1.054', 'biblio_id': 'USDA', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'cranberry-apple juice drink, bottled', 'g_ml': '1.063526774', 'specific_gravity': '1.0659', 'biblio_id': 'USDA', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'cream, 13% fat', 'g_ml': '1.013', 'specific_gravity': '', 'biblio_id': 'DK', 'category': 'Milk and dairy products'}, {'food_name': 'cream, 38% fat', 'g_ml': '0.984', 'specific_gravity': '', 'biblio_id': 'DK', 'category': 'Milk and dairy products'}, {'food_name': 'cream, 9% fat', 'g_ml': '1.017', 'specific_gravity': '', 'biblio_id': 'DK', 'category': 'Milk and dairy products'}, {'food_name': 'cream, heavy', 'g_ml': '0.994', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Milk and dairy products'}, {'food_name': 'cream, light', 'g_ml': '1.012', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Milk and dairy products'}, {'food_name': 'cream, sour (crème fraiche about 18% fat)', 'g_ml': '1.005', 'specific_gravity': '', 'biblio_id': 'DK', 'category': 'Milk and dairy products'}, {'food_name': 'cream, sour (crème fraiche about 38% fat)', 'g_ml': '0.978', 'specific_gravity': '', 'biblio_id': 'DK', 'category': 'Milk and dairy products'}, {'food_name': 'cream, whipped', 'g_ml': '0.496', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Milk and dairy products'}, {'food_name': 'donut mix', 'g_ml': '0.64', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'dough mix', 'g_ml': '0.59', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'dry flavoring mix roiko and other flavorings', 'g_ml': '0.7', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Herbes and spices'}, {'food_name': 'egg drop soup', 'g_ml': '1.017', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Soups'}, {'food_name': 'egg, chicken, boiled/poached', 'g_ml': '0.6', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Egg and egg products'}, {'food_name': 'egg, yoke, powder', 'g_ml': '0.37', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Egg and egg products'}, {'food_name': 'eggplant parmesan', 'g_ml': '0.825', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Mixed dishes'}, {'food_name': 'eggs, powdered', 'g_ml': '0.35', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Egg and egg products'}, {'food_name': 'finger millet, fermented flour', 'g_ml': '0.61', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Cereal and cereal products'}, {'food_name': 'flaxseed', 'g_ml': '0.7', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Nuts and seeds'}, {'food_name': 'french green beans', 'g_ml': '0.529999971', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Vegetables'}, {'food_name': 'fresh green peas (minji)', 'g_ml': '0.730000019', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Vegetables'}, {'food_name': 'fruit juice', 'g_ml': '1.06', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'garlic, flakes', 'g_ml': '0.35', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Herbes and spices'}, {'food_name': 'garlic, powder', 'g_ml': '0.32', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Herbes and spices'}, {'food_name': 'gelatin', 'g_ml': '0.72', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Miscellaneous foods'}, {'food_name': 'githeri (muthugo + beans) + meat', 'g_ml': '0.949999988', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'githeri (muthugo + beans) + meat + vegetable + potato/banana', 'g_ml': '0.99000001', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'githeri (muthugo + beans) + onion, boiled with fat', 'g_ml': '0.980000019', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'githeri (muthugo + beans) + potato/banana', 'g_ml': '0.879999995', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'githeri (muthugo + beans) + vegetable', 'g_ml': '1.039999962', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'githeri (muthugo + beans) + vegetable + meat', 'g_ml': '0.939999998', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'githeri + meat', 'g_ml': '0.75', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'githeri + meat + vegetable + potato/banana', 'g_ml': '1.049999952', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'githeri + onion, boiled with fat', 'g_ml': '0.829999983', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'githeri + peas', 'g_ml': '1.039999962', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'githeri + potato/banana', 'g_ml': '1.100000024', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'githeri + roots + vegetable', 'g_ml': '1.129999995', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'githeri + vegetable', 'g_ml': '1.299999952', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'githeri + vegetable + meat', 'g_ml': '0.839999974', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'githeri + vegetable + potato/banana', 'g_ml': '0.949999988', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'githeri plain (muthugo + beans + water)', 'g_ml': '0.980000019', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'githeri, beans + vegetable + potatoes', 'g_ml': '0.930000007', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'githeri, maize + peas', 'g_ml': '0.970000029', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'githeri, plain (maize + beans + water)', 'g_ml': '0.71', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'gitwero, banana + beans', 'g_ml': '1.200000048', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'gitwero, banana + beans + vegetable', 'g_ml': '1.200000048', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'gitwero, banana + potato + beans', 'g_ml': '1.039999962', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'gitwero, banana + vegetable', 'g_ml': '1.200000048', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'gitwero, banana, boiled with fat', 'g_ml': '1.190000057', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'gitwero, banana/potato', 'g_ml': '1.299999952', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'gitwero, banana/potato + meat', 'g_ml': '1.080000043', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'gitwero, banana/potato + vegetable', 'g_ml': '1.220000029', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'gitwero, root (yam, arrowroot, etc.)', 'g_ml': '1.139999986', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'gitwero, roots + banana', 'g_ml': '1.029999971', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'gitwero, roots + banana', 'g_ml': '1.029999971', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'glucolin, glucose', 'g_ml': '0.4', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Sweets'}, {'food_name': 'goat, intestine, boiled', 'g_ml': '0.56', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Meat and meat products'}, {'food_name': 'goat, intestine, raw', 'g_ml': '0.83', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Meat and meat products'}, {'food_name': 'grape juice', 'g_ml': '1.054', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'grape juice, canned or bottled, unsweetened, with added ascorbic acid', 'g_ml': '1.063526774', 'specific_gravity': '1.0659', 'biblio_id': 'USDA', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'grape juice, canned or bottled, unsweetened, without added ascorbic acid', 'g_ml': '1.063526774', 'specific_gravity': '1.0659', 'biblio_id': 'USDA', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'green bean casserole', 'g_ml': '0.95', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Mixed dishes'}, {'food_name': 'greengram, boiled', 'g_ml': '0.76', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Legumes'}, {'food_name': 'greengram, raw', 'g_ml': '0.79', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Legumes'}, {'food_name': 'guanabana nectar, canned', 'g_ml': '1.017679081', 'specific_gravity': '1.01995', 'biblio_id': 'USDA', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'guava nectar, canned', 'g_ml': '1.022667949', 'specific_gravity': '1.02495', 'biblio_id': 'USDA', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'ice cream ', 'g_ml': '0.554', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Milk and dairy products'}, {'food_name': 'ice cream, light (formerly ice milk)', 'g_ml': '0.555314851', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Milk and dairy products'}, {'food_name': 'ice cream, light, no sugar added', 'g_ml': '0.579724295', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Milk and dairy products'}, {'food_name': 'ice cream, no sugar added', 'g_ml': '0.537007768', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Milk and dairy products'}, {'food_name': 'ice cream, regular', 'g_ml': '0.561417212', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Milk and dairy products'}, {'food_name': 'ice cream, rich', 'g_ml': '0.622440822', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Milk and dairy products'}, {'food_name': 'ice, crushed', 'g_ml': '0.64', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'jam ', 'g_ml': '1.333', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Sweets'}, {'food_name': 'jam, sweetened', 'g_ml': '1.43', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Sweets'}, {'food_name': 'jelly ', 'g_ml': '1.245', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Sweets'}, {'food_name': 'juice, apple and grape blend, with added ascorbic acid', 'g_ml': '1.048111173', 'specific_gravity': '1.05045', 'biblio_id': 'USDA', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'juice, apple, grape and pear blend, with added ascorbic acid and calcium', 'g_ml': '1.049657722', 'specific_gravity': '1.052', 'biblio_id': 'USDA', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'kidney beans, dry, boiled', 'g_ml': '0.790000021', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Legumes'}, {'food_name': 'kidney beans, dry, raw', 'g_ml': '0.75', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Legumes'}, {'food_name': 'kidney beans, green, boiled', 'g_ml': '0.7', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Legumes'}, {'food_name': 'kidney beans, green, raw', 'g_ml': '0.68', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Legumes'}, {'food_name': 'lard', 'g_ml': '0.919', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Oils and fats'}, {'food_name': 'lasagna', 'g_ml': '1.042', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Mixed dishes'}, {'food_name': 'leaves, managu, raw (black night shade)', 'g_ml': '0.2', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Vegetables'}, {'food_name': 'leaves, onion, spring onion, raw', 'g_ml': '0.44', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Vegetables'}, {'food_name': 'lemonade, frozen concentrate, pink', 'g_ml': '1.23723914', 'specific_gravity': '1.24', 'biblio_id': 'USDA', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'lemonade, frozen concentrate, white', 'g_ml': '1.167345106', 'specific_gravity': '1.16995', 'biblio_id': 'USDA', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'lentils, green, small, boiled', 'g_ml': '0.85', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Legumes'}, {'food_name': 'lentils, green, small, raw', 'g_ml': '0.89', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Legumes'}, {'food_name': 'liqueur', 'g_ml': '1.09', 'specific_gravity': '', 'biblio_id': 'DK', 'category': 'Beverages, alcoholic'}, {'food_name': 'loquat', 'g_ml': '0.6', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Fruits'}, {'food_name': 'macaroni and cheese, canned', 'g_ml': '0.996', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Mixed dishes'}, {'food_name': 'mango nectar, canned', 'g_ml': '0.997723611', 'specific_gravity': '0.99995', 'biblio_id': 'USDA', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'mataha (maize stew) (maize stew), maize + peas', 'g_ml': '0.860000014', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'mataha (maize stew), beans + banana', 'g_ml': '1.220000029', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'mataha (maize stew), beans + banana + potato', 'g_ml': '1.25', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'mataha (maize stew), beans + banana + potato + vegetable', 'g_ml': '1.149999976', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'mataha (maize stew), beans + potato/banana + vegetable', 'g_ml': '1.139999986', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'mataha (maize stew), beans + vegetable', 'g_ml': '1.019999981', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'mataha (maize stew), beans + vegetable + banana', 'g_ml': '1', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'mataha (maize stew), maize + banana', 'g_ml': '1.090000033', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'mataha (maize stew), maize + banana/potato + vegetable', 'g_ml': '1.100000024', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'mataha (maize stew), maize + beans + potato', 'g_ml': '0.75', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'mataha (maize stew), maize + beans + potato + vegetable', 'g_ml': '0.949999988', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'mataha (maize stew), maize + beans + potato, boiled with fat', 'g_ml': '0.75', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'mataha (maize stew), maize + beans + vegetable + banana', 'g_ml': '0.699999988', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'mataha (maize stew), maize + vegetable', 'g_ml': '0.899999976', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'mataha (maize stew), paw paw', 'g_ml': '1.330000043', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'mayonnaise, light', 'g_ml': '1', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Oils and fats'}, {'food_name': 'mayonnaise, traditional', 'g_ml': '0.91', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Oils and fats'}, {'food_name': 'meal supplement drink, nestle, supligen, canned, peanut flavor', 'g_ml': '1.037634551', 'specific_gravity': '1.03995', 'biblio_id': 'USDA', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'mexican casserole w/beef, beans, cheese, chips', 'g_ml': '0.6', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Mixed dishes'}, {'food_name': 'milk (non-fat dry)', 'g_ml': '0.56', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Milk and dairy products'}, {'food_name': 'milk (powdered whole)', 'g_ml': '0.56', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Milk and dairy products'}, {'food_name': 'milk (powdered)', 'g_ml': '0.21', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Milk and dairy products'}, {'food_name': 'milk shake, fruit and other', 'g_ml': '1', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Milk and dairy products'}, {'food_name': 'milk, acidophilus cultured', 'g_ml': '1.01', 'specific_gravity': '', 'biblio_id': 'DK', 'category': 'Milk and dairy products'}, {'food_name': 'milk, buttermilk', 'g_ml': '1.022', 'specific_gravity': '', 'biblio_id': 'DK', 'category': 'Milk and dairy products'}, {'food_name': 'milk, chocolate milk, skimmed', 'g_ml': '1.056', 'specific_gravity': '', 'biblio_id': 'DK', 'category': 'Milk and dairy products'}, {'food_name': 'milk, cow, whole', 'g_ml': '1.039999962', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Milk and dairy products'}, {'food_name': 'milk, goat, whole', 'g_ml': '1.08', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Milk and dairy products'}, {
        'food_name': 'milk, liquid, partially skimmed', 'g_ml': '1.034', 'specific_gravity': '', 'biblio_id': 'DK', 'category': 'Milk and dairy products'}, {'food_name': 'milk, liquid, skimmed', 'g_ml': '1.033', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Milk and dairy products'}, {'food_name': 'milk, liquid, skimmed', 'g_ml': '1.036', 'specific_gravity': '', 'biblio_id': 'DK', 'category': 'Milk and dairy products'}, {'food_name': 'milk, liquid, whole', 'g_ml': '1.03', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Milk and dairy products'}, {'food_name': 'milk, liquid, whole', 'g_ml': '1.031', 'specific_gravity': '', 'biblio_id': 'DK', 'category': 'Milk and dairy products'}, {'food_name': 'millet', 'g_ml': '0.64', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'millet', 'g_ml': '0.64', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Cereal and cereal products'}, {'food_name': 'millet flour, bulrush', 'g_ml': '0.560000002', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Cereal and cereal products'}, {'food_name': 'millet flour, finger', 'g_ml': '0.610000014', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Cereal and cereal products'}, {'food_name': 'millet, bulrush', 'g_ml': '0.899999976', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Cereal and cereal products'}, {'food_name': 'millet, finger', 'g_ml': '0.810000002', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Cereal and cereal products'}, {'food_name': 'mini ravioli, canned', 'g_ml': '1.046', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Mixed dishes'}, {'food_name': 'miso, broth, ready to drink', 'g_ml': '1.06', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Tea, cacao, coffee and drinking powders'}, {'food_name': 'monosodium glutamate', 'g_ml': '1.62', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Miscellaneous foods'}, {'food_name': 'moussaka', 'g_ml': '0.846', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Mixed dishes'}, {'food_name': 'mushroom soup', 'g_ml': '1.017', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Soups'}, {'food_name': 'mustard powdered', 'g_ml': '0.26', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Miscellaneous foods'}, {'food_name': 'muthugo (maize without germ and cover) only', 'g_ml': '0.75999999', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'noodles/pasta with fat', 'g_ml': '0.800000012', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'nutella', 'g_ml': '1.26', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Sweets'}, {'food_name': 'nuts', 'g_ml': '0.63', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Nuts and seeds'}, {'food_name': 'oat flour', 'g_ml': '0.53', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'oat middlings', 'g_ml': '0.61', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'oats', 'g_ml': '0.41', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Cereal and cereal products'}, {'food_name': 'oats', 'g_ml': '0.43', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'oats groats, whole', 'g_ml': '0.74', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'oats, ground', 'g_ml': '0.46', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'oats, hulls', 'g_ml': '0.13', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'oats, rolled', 'g_ml': '0.34', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'oil, other than palmoil', 'g_ml': '0.92', 'specific_gravity': '', 'biblio_id': 'DK', 'category': 'Oils and fats'}, {'food_name': 'oil, palmoil', 'g_ml': '0.89', 'specific_gravity': '', 'biblio_id': 'DK', 'category': 'Oils and fats'}, {'food_name': 'oil, sunflower', 'g_ml': '0.96', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Oils and fats'}, {'food_name': 'oil, vegetable, coconut', 'g_ml': '0.924', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Oils and fats'}, {'food_name': 'oil, vegetable, corn', 'g_ml': '0.922', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Oils and fats'}, {'food_name': 'oil, vegetable, olive', 'g_ml': '0.918', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Oils and fats'}, {'food_name': 'oil, vegetable, palm', 'g_ml': '0.915', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Oils and fats'}, {'food_name': 'oil, vegetable, peanut', 'g_ml': '0.914', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Oils and fats'}, {'food_name': 'oil, vegetable, soya', 'g_ml': '0.927', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Oils and fats'}, {'food_name': 'olives, green, with stone', 'g_ml': '0.65', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Vegetables'}, {'food_name': 'onions, chopped', 'g_ml': '0.22', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Vegetables'}, {'food_name': 'onions, fried, cubed', 'g_ml': '0.75', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Vegetables'}, {'food_name': 'onions, minced', 'g_ml': '0.13', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Vegetables'}, {'food_name': 'onions, powdered', 'g_ml': '0.4', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Vegetables'}, {'food_name': 'onions, raw, cubed', 'g_ml': '0.55', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Vegetables'}, {'food_name': 'orange juice', 'g_ml': '1.038', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'orange juice with calcium', 'g_ml': '1.038', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'orange juice, canned, unsweetened', 'g_ml': '1.042906121', 'specific_gravity': '1.045233333', 'biblio_id': 'USDA', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'orange soda (sweetened with sugar)', 'g_ml': '1.029', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'pasta, short macaroni style, boiled', 'g_ml': '0.55', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Cereal and cereal products'}, {'food_name': 'pasta, short macaroni style, raw', 'g_ml': '0.39', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Cereal and cereal products'}, {'food_name': 'pasta/ noodles, boiled', 'g_ml': '0.589999974', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Cereal and cereal products'}, {'food_name': 'paw paw, unripe', 'g_ml': '0.56', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Fruits'}, {'food_name': 'peanuts', 'g_ml': '0.53', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Nuts and seeds'}, {'food_name': 'peanuts, shelled', 'g_ml': '0.69', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Nuts and seeds'}, {'food_name': 'peanuts, unshelled', 'g_ml': '0.325', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Nuts and seeds'}, {'food_name': 'pigeon peas, boiled', 'g_ml': '0.75', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Legumes'}, {'food_name': 'pigeon peas, raw', 'g_ml': '0.84', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Legumes'}, {'food_name': 'pistachio, raw, with shell', 'g_ml': '0.6', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Nuts and seeds'}, {'food_name': 'pistachio, raw, without shell', 'g_ml': '0.646', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Nuts and seeds'}, {'food_name': 'pork, fatty, with bone, boiled', 'g_ml': '0.63', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Meat and meat products'}, {'food_name': 'pork, fatty, with bone, raw', 'g_ml': '0.97', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Meat and meat products'}, {'food_name': 'pork, medium, with bone, boiled', 'g_ml': '0.7', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Meat and meat products'}, {'food_name': 'pork, medium, with bone, raw', 'g_ml': '0.93', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Meat and meat products'}, {'food_name': 'porridge flour bonavist, boiled', 'g_ml': '0.730000019', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Cereal and cereal products'}, {'food_name': 'porridge flour bonavist, raw', 'g_ml': '0.839999974', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Cereal and cereal products'}, {'food_name': 'porridge flour ken-uji + lemon extract', 'g_ml': '0.540000021', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Cereal and cereal products'}, {'food_name': 'porridge flour ken-uji:f.mill, bul, sorg, wheat', 'g_ml': '0.600000024', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Cereal and cereal products'}, {'food_name': 'porridge, maize, flour + water', 'g_ml': '1.049999952', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Cereal and cereal products'}, {'food_name': 'potato chips', 'g_ml': '0.09', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Snacks'}, {'food_name': 'potato chips, pringles', 'g_ml': '0.12', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Snacks'}, {'food_name': 'potato, english, boiled', 'g_ml': '0.59', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Tubers and products'}, {'food_name': 'potato, english, raw', 'g_ml': '0.589999974', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Tubers and products'}, {'food_name': 'potatoes, flakes', 'g_ml': '0.21', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Tubers and products'}, {'food_name': 'potatoes, powdered', 'g_ml': '0.77', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Tubers and products'}, {'food_name': 'powder, chocolate drinking powder', 'g_ml': '0.525', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Tea, cacao, coffee and drinking powders'}, {'food_name': 'powders', 'g_ml': '0.225', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Tea, cacao, coffee and drinking powders'}, {'food_name': 'prawns, whole, boiled, with shell', 'g_ml': '0.58', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Fish and fish products'}, {'food_name': 'prawns, whole, boiled, without shell', 'g_ml': '0.77', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Fish and fish products'}, {'food_name': 'protein supplement', 'g_ml': '0.54', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Miscellaneous foods'}, {'food_name': 'quaker oats, propel fitness water, fruit-flavored, non-carbonated', 'g_ml': '1.000218045', 'specific_gravity': '1.00245', 'biblio_id': 'USDA', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'rapeseed', 'g_ml': '0.77', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Nuts and seeds'}, {'food_name': 'rice', 'g_ml': '0.72', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'rice + beans', 'g_ml': '0.75', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'rice + beans + potato/banana', 'g_ml': '0.850000024', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'rice + meat', 'g_ml': '0.730000019', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'rice + meat + vegetable', 'g_ml': '0.829999983', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'rice + potato/banana', 'g_ml': '0.800000012', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'rice + roots (yam, arrowroot etc.)', 'g_ml': '0.899999976', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'rice + vegetable', 'g_ml': '0.649999976', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'rice + vegetable + potato/banana', 'g_ml': '0.800000012', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'rice, boiled', 'g_ml': '0.73', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Cereal and cereal products'}, {'food_name': 'rice, boiled with fat', 'g_ml': '0.699999988', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Cereal and cereal products'}, {'food_name': 'rice, bran', 'g_ml': '0.42', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'rice, hulled', 'g_ml': '0.75', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Cereal and cereal products'}, {'food_name': 'rice, plain (rice + water)', 'g_ml': '0.699999988', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'rice, puffed', 'g_ml': '0.1', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'rice, raw', 'g_ml': '0.85', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Cereal and cereal products'}, {'food_name': 'rice, rough', 'g_ml': '0.58', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Cereal and cereal products'}, {'food_name': 'rice, white, boiled', 'g_ml': '0.73', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Cereal and cereal products'}, {'food_name': 'rice, white, raw', 'g_ml': '0.82', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Cereal and cereal products'}, {'food_name': 'rye', 'g_ml': '0.72', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Cereal and cereal products'}, {'food_name': 'rye, bran', 'g_ml': '0.28', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'rye, flour ', 'g_ml': '0.67', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'rye, malted', 'g_ml': '0.51', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'rye, middlings', 'g_ml': '0.67', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'rye, shorts', 'g_ml': '0.54', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'rye, whole', 'g_ml': '0.705', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'sage, leaves', 'g_ml': '0.29', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Herbes and spices'}, {'food_name': 'salad dressing', 'g_ml': '1.1', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Miscellaneous foods'}, {'food_name': 'salad, green, leaves, raw', 'g_ml': '0.06', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Vegetables'}, {'food_name': 'salt, fine table', 'g_ml': '1.38', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Miscellaneous foods'}, {'food_name': 'salt, granulated', 'g_ml': '1.28', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Miscellaneous foods'}, {'food_name': 'salt, sodium chloride', 'g_ml': '2.165', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Miscellaneous foods'}, {'food_name': 'salt, table', 'g_ml': '1.217', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Miscellaneous foods'}, {'food_name': 'sauce, soy', 'g_ml': '1.12', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Miscellaneous foods'}, {'food_name': 'semolina, raw', 'g_ml': '0.78', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Cereal and cereal products'}, {'food_name': 'snacks, puffed, lowfat', 'g_ml': '0.11', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Snacks'}, {'food_name': 'sodium bicarbonate', 'g_ml': '2.2', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Miscellaneous foods'}, {'food_name': 'soft drinks, diet soda', 'g_ml': '0.988', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'solid vegetable fat kimbo', 'g_ml': '0.6', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Oils and fats'}, {'food_name': 'solid vegetable fat rina ', 'g_ml': '0.67', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Oils and fats'}, {'food_name': 'sorghum, fermented flour', 'g_ml': '0.54', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Cereal and cereal products'}, {'food_name': 'sorghum, flour', 'g_ml': '0.540000021', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Cereal and cereal products'}, {'food_name': 'sorghum, seed', 'g_ml': '0.535', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'soup, meat', 'g_ml': '1.039999962', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Soups'}, {'food_name': 'soup, mixed', 'g_ml': '1.049999952', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Soups'}, {'food_name': 'soup, thick (squash, potato)', 'g_ml': '1.09', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Soups'}, {'food_name': 'soup, vegetable', 'g_ml': '0.99000001', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Soups'}, {'food_name': 'sour milk, cow, whole', 'g_ml': '0.980000019', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Milk and dairy products'}, {'food_name': 'soy drink', 'g_ml': '1.08', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'soy, flour ', 'g_ml': '0.7', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'soya + milk + sugar', 'g_ml': '1.05', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'soya + sugar', 'g_ml': '1.05', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'soya, flour ', 'g_ml': '0.64', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'soybean', 'g_ml': '0.74', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Legumes'}, {'food_name': 'soybean, boiled', 'g_ml': '0.790000021', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Legumes'}, {'food_name': 'soybean, boiled with fat', 'g_ml': '0.699999988', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Legumes'}, {'food_name': 'soybean, flakes', 'g_ml': '0.58', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Legumes'}, {'food_name': 'soybean, hulls', 'g_ml': '0.4', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Legumes'}, {'food_name': 'soybean, meal', 'g_ml': '0.64', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Legumes'}, {'food_name': 'spaghetti and meat balls, canned', 'g_ml': '1.038', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Mixed dishes'}, {'food_name': 'spice, barbecue', 'g_ml': '0.48', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Herbes and spices'}, {'food_name': 'spice, blend', 'g_ml': '0.58', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Herbes and spices'}, {'food_name': 'spinach, frozen, cooked', 'g_ml': '1.046', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Vegetables'}, {'food_name': 'spinach, leaves, raw', 'g_ml': '0.08', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Vegetables'}, {'food_name': 'spirits, 45% alcohol (whiskey)', 'g_ml': '0.939', 'specific_gravity': '', 'biblio_id': 'DK', 'category': 'Beverages, alcoholic'}, {'food_name': 'spirits, 70% alcohol', 'g_ml': '0.885', 'specific_gravity': '', 'biblio_id': 'DK', 'category': 'Beverages, alcoholic'}, {'food_name': 'spirits, 75% alcohol', 'g_ml': '0.873', 'specific_gravity': '', 'biblio_id': 'DK', 'category': 'Beverages, alcoholic'}, {'food_name': 'sports drink, coca-cola, powerade, lemon-lime flavored, ready-to-drink', 'g_ml': '1.027606928', 'specific_gravity': '1.0299', 'biblio_id': 'USDA', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'sports drink, pepsico quaker gatorade, gatorade, original, fruit-flavored, ready-to-drink', 'g_ml': '1.027606928', 'specific_gravity': '1.0299', 'biblio_id': 'USDA', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'stew, banana', 'g_ml': '1.070000052', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'stew, banana + potato + vegetable', 'g_ml': '1.059999943', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'stew, beans', 'g_ml': '1.01', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'stew, beans/ peas + meat + vegetables', 'g_ml': '0.939999998', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'stew, beans/ peas + vegetables', 'g_ml': '1.070000052', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'stew, meat', 'g_ml': '1.120000005', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'stew, pea + potato/banana', 'g_ml': '1.100000024', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'stew, pea + potato/banana + vegetable', 'g_ml': '1.220000029', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'stew, potato', 'g_ml': '1.100000024', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'stew, potato + beans + vegetable', 'g_ml': '1.080000043', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'stew, vegetable', 'g_ml': '0.680000007', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'stew, vegetable + meat', 'g_ml': '0.860000014', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'stew, vegetable + potato', 'g_ml': '1.100000024', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'stew, vegetable + potato + meat', 'g_ml': '1.080000043', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'stew: eggs + veg', 'g_ml': '0.68', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'sucrose', 'g_ml': '0.85', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Sweets'}, {'food_name': 'sucrose octoacetate', 'g_ml': '0.53', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Sweets'}, {'food_name': 'sugar', 'g_ml': '0.95', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Sweets'}, {'food_name': 'sugar, dextrose', 'g_ml': '0.62', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Sweets'}, {'food_name': 'sugar, dextrose', 'g_ml': '0.58', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Sweets'}, {'food_name': 'sugar, granulated', 'g_ml': '0.7', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Sweets'}, {'food_name': 'sugar, powdered', 'g_ml': '0.56', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Sweets'}, {'food_name': 'sugar, white', 'g_ml': '0.9', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Sweets'}, {'food_name': 'sugar, white', 'g_ml': '0.88', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Sweets'}, {'food_name': 'sunflower, seed', 'g_ml': '0.62', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Nuts and seeds'}, {'food_name': 'sweet pepper, raw, cubes', 'g_ml': '0.51', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Vegetables'}, {'food_name': 'sweet pepper, raw, half rings', 'g_ml': '0.39', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Vegetables'}, {'food_name': 'sweet potato, boiled', 'g_ml': '0.65', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Tubers and products'}, {'food_name': 'sweet potato, raw', 'g_ml': '0.44', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Tubers and products'}, {'food_name': 'syrup, corn', 'g_ml': '1.38', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Sweets'}, {'food_name': 'syrup, corn, light', 'g_ml': '1.404266424', 'specific_gravity': '1.4074', 'biblio_id': 'USDA', 'category': 'Sweets'}, {'food_name': 'syrup, fruit, blackberry', 'g_ml': '1.34', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Sweets'}, {'food_name': 'syrup, maple', 'g_ml': '1.318690717', 'specific_gravity': '1.321633333', 'biblio_id': 'USDA', 'category': 'Sweets'}, {'food_name': 'syrup, pancake ', 'g_ml': '1.312', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Sweets'}, {'food_name': 'tamarind nectar, canned', 'g_ml': '1.012690214', 'specific_gravity': '1.01495', 'biblio_id': 'USDA', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'tea, black (tea leaves)', 'g_ml': '0.48', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Tea, cacao, coffee and drinking powders'}, {'food_name': 'tea, flakes', 'g_ml': '0.38', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Tea, cacao, coffee and drinking powders'}, {'food_name': 'tea, herbal, ciakimora (leaves + water)', 'g_ml': '1', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Tea, cacao, coffee and drinking powders'}, {'food_name': 'tea, herbal, ciakimora leaves ', 'g_ml': '0.23', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Tea, cacao, coffee and drinking powders'}, {'food_name': 'tea, liquid', 'g_ml': '1', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Tea, cacao, coffee and drinking powders'}, {'food_name': 'tea, only (tea leaves + water)', 'g_ml': '1', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Tea, cacao, coffee and drinking powders'}, {'food_name': 'tea, powdered', 'g_ml': '0.43', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Tea, cacao, coffee and drinking powders'}, {'food_name': 'tea, ready-to-drink, arizona iced tea, with lemon flavor', 'g_ml': '1.033693346', 'specific_gravity': '1.036', 'biblio_id': 'USDA', 'category': 'Tea, cacao, coffee and drinking powders'}, {'food_name': 'tea, ready-to-drink, lipton brisk iced tea, with lemon flavor', 'g_ml': '1.031697799', 'specific_gravity': '1.034', 'biblio_id': 'USDA', 'category': 'Tea, cacao, coffee and drinking powders'}, {'food_name': 'tea, ready-to-drink, nestle, cool nestea ice tea lemon flavor', 'g_ml': '1.033693346', 'specific_gravity': '1.036', 'biblio_id': 'USDA', 'category': 'Tea, cacao, coffee and drinking powders'}, {'food_name': 'tomato soup', 'g_ml': '1.017', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Soups'}, {'food_name': 'tuna noodle casserole', 'g_ml': '0.933', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Mixed dishes'}, {'food_name': 'ugali + beans', 'g_ml': '0.800000012', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'ugali + beans + vegetable', 'g_ml': '0.800000012', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'ugali + vegetable, crumbed', 'g_ml': '0.75', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'ugali + vegetables, boiled with fat', 'g_ml': '1.200000048', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'ugali, plain (flour + water), crumbed', 'g_ml': '0.75', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Mixed dishes'}, {'food_name': 'vitamin additive', 'g_ml': '0.66', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Miscellaneous foods'}, {'food_name': 'vitamin compound', 'g_ml': '0.67', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Miscellaneous foods'}, {'food_name': 'vitamin enrichment', 'g_ml': '0.64', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Miscellaneous foods'}, {'food_name': 'vitamin mix', 'g_ml': '0.7', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Miscellaneous foods'}, {'food_name': 'vitamin powder', 'g_ml': '0.56', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Miscellaneous foods'}, {'food_name': 'water, ice, 0\xa0°c', 'g_ml': '0.916', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'water, ice, 4\xa0°c', 'g_ml': '0.999', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'water, liquid, 20\xa0°c', 'g_ml': '0.998', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'water, mineralwater', 'g_ml': '1.0375', 'specific_gravity': '', 'biblio_id': 'DK', 'category': 'Beverages, non alcoholic (including soft drinks and juices)'}, {'food_name': 'wheat', 'g_ml': '0.77', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Cereal and cereal products'}, {'food_name': 'wheat, bran', 'g_ml': '0.22', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'wheat, cracked', 'g_ml': '0.56', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'wheat, cut', 'g_ml': '0.74', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'wheat, flour', 'g_ml': '0.48', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'wheat, flour', 'g_ml': '0.579999983', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Cereal and cereal products'}, {'food_name': 'wheat, flour ', 'g_ml': '0.67', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'wheat, flour ', 'g_ml': '0.521', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Cereal and cereal products'}, {'food_name': 'wheat, flour, malted', 'g_ml': '0.66', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'wheat, flour, white', 'g_ml': '0.67', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Cereal and cereal products'}, {'food_name': 'wheat, flour, wholemeal', 'g_ml': '0.55', 'specific_gravity': '', 'biblio_id': 'RC', 'category': 'Cereal and cereal products'}, {'food_name': 'wheat, gluten', 'g_ml': '0.69', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'wheat, hulls', 'g_ml': '0.7', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'wheat, middlings', 'g_ml': '0.24', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'wheat, shaved', 'g_ml': '0.54', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'wheat, whole', 'g_ml': '0.775', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'whey', 'g_ml': '0.56', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Cereal and cereal products'}, {'food_name': 'wieners and sauerkraut (mixture)', 'g_ml': '0.612', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Mixed dishes'}, {'food_name': 'wine, table, all', 'g_ml': '0.992595117', 'specific_gravity': '0.994810061', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'wine, table, red', 'g_ml': '0.991672652', 'specific_gravity': '0.993885539', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'wine, table, red, barbera', 'g_ml': '0.992073719', 'specific_gravity': '0.9942875', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'wine, table, red, burgundy', 'g_ml': '0.996547664', 'specific_gravity': '0.998771429', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'wine, table, red, cabernet franc', 'g_ml': '0.990925448', 'specific_gravity': '0.993136667', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'wine, table, red, cabernet sauvignon', 'g_ml': '0.991801415', 'specific_gravity': '0.994014589', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'wine, table, red, carignane', 'g_ml': '0.992784633', 'specific_gravity': '0.995', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'wine, table, red, claret', 'g_ml': '0.99370077', 'specific_gravity': '0.995918182', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'wine, table, red, gamay', 'g_ml': '0.991574001', 'specific_gravity': '0.993786667', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'wine, table, red, lemberger', 'g_ml': '0.993337943', 'specific_gravity': '0.995554546', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'wine, table, red, merlot', 'g_ml': '0.991254947', 'specific_gravity': '0.993466901', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'wine, table, red, mouvedre', 'g_ml': '0.99098864', 'specific_gravity': '0.9932', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'wine, table, red, petite sirah', 'g_ml': '0.993794379', 'specific_gravity': '0.996012', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'wine, table, red, pinot noir', 'g_ml': '0.990556156', 'specific_gravity': '0.992766551', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'wine, table, red, sangiovese', 'g_ml': '0.991159687', 'specific_gravity': '0.993371429', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'wine, table, red, syrah', 'g_ml': '0.99181014', 'specific_gravity': '0.994023333', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'wine, table, red, zinfandel', 'g_ml': '0.992086191', 'specific_gravity': '0.9943', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'wine, table, white', 'g_ml': '0.992545666', 'specific_gravity': '0.9947605', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'wine, table, white, chardonnay', 'g_ml': '0.989190074', 'specific_gravity': '0.991397421', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'wine, table, white, chenin blanc', 'g_ml': '0.995476063', 'specific_gravity': '0.997697436', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'wine, table, white, fume blanc', 'g_ml': '0.990015811', 'specific_gravity': '0.992225', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'wine, table, white, gewurztraminer', 'g_ml': '0.994750833', 'specific_gravity': '0.996970588', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'wine, table, white, late harvest', 'g_ml': '1.038375206', 'specific_gravity': '1.040692308', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'wine, table, white, late harvest, gewurztraminer', 'g_ml': '1.02903707', 'specific_gravity': '1.031333333', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'wine, table, white, muller thurgau', 'g_ml': '0.996791077', 'specific_gravity': '0.999015385', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'wine, table, white, muscat', 'g_ml': '1.011014224', 'specific_gravity': '1.01327027', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'wine, table, white, pinot blanc', 'g_ml': '0.988857033', 'specific_gravity': '0.991063636', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'wine, table, white, pinot gris (grigio)', 'g_ml': '0.988829628', 'specific_gravity': '0.99103617', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'wine, table, white, riesling', 'g_ml': '0.997961437', 'specific_gravity': '1.000188356', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'wine, table, white, sauvignon blanc', 'g_ml': '0.990176753', 'specific_gravity': '0.992386301', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'wine, table, white, semillon', 'g_ml': '0.995414248', 'specific_gravity': '0.997635484', 'biblio_id': 'USDA', 'category': 'Beverages, alcoholic'}, {'food_name': 'wine, white', 'g_ml': '1.02', 'specific_gravity': '', 'biblio_id': 'DK', 'category': 'Beverages, alcoholic'}, {'food_name': 'yam, boiled', 'g_ml': '0.79', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Tubers and products'}, {'food_name': 'yam, raw', 'g_ml': '0.66', 'specific_gravity': '', 'biblio_id': 'KEN', 'category': 'Tubers and products'}, {'food_name': 'yeast', 'g_ml': '0.95', 'specific_gravity': '', 'biblio_id': 'ASI', 'category': 'Miscellaneous foods'}, {'food_name': 'yoghurt, berry, low fat, artificially sweetened', 'g_ml': '1.06', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Milk and dairy products'}, {'food_name': 'yoghurt, fruits', 'g_ml': '1.0525', 'specific_gravity': '', 'biblio_id': 'DK', 'category': 'Milk and dairy products'}, {'food_name': 'yoghurt, plain, unsweetened', 'g_ml': '1.06', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Milk and dairy products'}, {'food_name': 'yoghurt, plain, unsweetened', 'g_ml': '1.031', 'specific_gravity': '', 'biblio_id': 'DK', 'category': 'Milk and dairy products'}, {'food_name': 'yoghurt, strawberry, low fat', 'g_ml': '1.08', 'specific_gravity': '', 'biblio_id': 'FNDDS 4.1', 'category': 'Milk and dairy products'}, {'food_name': 'zesty italian ‘‘hamburger helper’’', 'g_ml': '1.038', 'specific_gravity': '', 'biblio_id': 'S&W', 'category': 'Mixed dishes'}]
    return csv_data


class main_app(toga.App):

    async def import_data(self, widget) -> None:
        """On Android, let user pick a file to restore history from."""
        print("current_platform : ", current_platform)
        if current_platform == "android":
            from android.content import Intent

            fileChose = Intent(Intent.ACTION_GET_CONTENT)
            fileChose.addCategory(Intent.CATEGORY_OPENABLE)
            fileChose.setType("*/*")
            results = await self._impl.intent_result(Intent.createChooser(fileChose, "Choose a file"))
            data = results['resultData'].getData()
            context = self._impl.native

            bytesJarray = bytes((context.getContentResolver().openInputStream(data).readAllBytes()))
            data = pickle.loads(bytesJarray)  # Convert bytes to string
            for item in data:
                self.history_item_selection.data.append({
                    "unit_selection": item['unit_selection'],
                    "unit_value": item['unit_value'],
                    "density_selection": item['density_selection'],
                    "comment": item['comment']
                })
        else:
            pass
        return

    async def export_data(self, widget) -> None:
        epoch_time = str(int(time.time()))            
        print("current_platform : ", current_platform)
        if current_platform == "android":
            from android.content import Intent

            # Create an intent to open a system file picker
            context = self._impl.native
            default_file_name = f'quick_food_price_comparison_{epoch_time}.pickle'
            intent = Intent(Intent.ACTION_CREATE_DOCUMENT)
            intent.addCategory(Intent.CATEGORY_OPENABLE)
            intent.setType('application/octet-stream')
            intent.putExtra(Intent.EXTRA_TITLE, default_file_name)

            # Start the intent and get the result
            results = await self._impl.intent_result(intent)
            uri = results['resultData'].getData()

            # Copy the file to the selected location
            # input_stream = context.getContentResolver().openInputStream(Uri.fromFile(File(file_path)))
            output_stream = context.getContentResolver().openOutputStream(uri)
            output_stream.write(self.convert_history_to_pickle())
            output_stream.close()
            #input_stream.close()
            output_stream.close()

            print(f'Saved {byte_count} bytes to {uri.toString()}')
        else:
            pass

    def define_local_data(self) -> None:
        """Retrieve the platforms local data path and create it if necessary."""
        self.location = Path(str(self.paths.data) +
                             '\conversion_history.pickle')
        directory = os.path.dirname(self.location)
        if not os.path.exists(directory):
            # If the directory does not exist, create it
            os.makedirs(directory)

    def load_history_from_pickle(self, location=None):
        """Read history data saved in a pickle file."""
        if location == None:
            location = self.location
        print(location)
        with open(location, 'rb') as handle:
            data = pickle.load(handle)

        return data

    def convert_history_to_pickle(self, location=None):
        """Take a dictionary of the history and save it to a pickle file locally."""
        pickleable_dict = []
        for row in self.history_item_selection.data:
            pickleable_dict.append({
                "unit_selection": row.unit_selection,
                "unit_value": row.unit_value,
                "density_selection": row.density_selection,
                "comment": row.comment
            })
        pickleable_dict = [i for n, i in enumerate(
            pickleable_dict) if i not in pickleable_dict[n + 1:]]
        if location == None:
            with open(self.location, 'wb+') as handle:
                pickle.dump(pickleable_dict, handle,
                            protocol=pickle.HIGHEST_PROTOCOL)        
        return pickle.dumps(pickleable_dict, protocol=pickle.HIGHEST_PROTOCOL)

    def cleanup_conversion_history(self) -> None:
        """Get rid of duplicate records before they are written to the history table."""
        for row in self.history_item_selection.data:
            if row.density_selection is None and row.unit_selection is None and row.unit_value is None:
                self.history_item_selection.data.remove(row=row)
            elif row.density_selection == self.density_item_selection.value.food_name and \
                    row.unit_selection == self.unit_selection.value.name and \
                    row.unit_value == self.item_cost_input.value:
                self.history_item_selection.data.remove(row=row)
        return

    def clear_history(self, button) -> None:
        """Delete the history file and remove all items from the table."""
        if Path.exists(self.location):
            self.location.unlink()
        while self.history_item_selection.data:
            for row in self.history_item_selection.data:
                self.history_item_selection.data.remove(row=row)

    def reset_input(self, button) -> None:
        """Reset the input boxes and choices."""
        self.item_cost_input.value = 1
        self.unit_selection.value = self.unit_selection.items[0]
        self.density_item_selection.value = self.density_item_selection.items[0]
        self.clean_menu_items()
        self.clear_button.style.visibility = 'hidden'
    

    def load_history(self, *kwargs) -> None:
        """Take a value from the history table and load it into the input boxes."""
        if self.history_item_selection.selection.unit_selection:
            self.item_cost_input.value = self.history_item_selection.selection.unit_value
            # Lookup mass value and reassign
            for index, value in enumerate(selection_list):
                if value['name'] == str(self.history_item_selection.selection.unit_selection):
                    self.unit_selection.value = self.unit_selection.items[index]
            # Lookup desnity value and reassign
            for index, value in enumerate(self.food_items):
                if value['food_name'] == str(self.history_item_selection.selection.density_selection):
                    self.density_item_selection.value = self.density_item_selection.items[index]
            self.comment_input.value = self.history_item_selection.selection.comment
            self.perform_conversion()
        else:
            print('Nothing selected.')

    def write_history(self) -> None:
        """Write history to a pickle file after cleaning it up. Once done go to the latest menu item."""
        self.cleanup_conversion_history()
        self.history_item_selection.data.append({
            "unit_selection": self.unit_selection.value.name,
            "unit_value": self.item_cost_input.value,
            "density_selection": self.density_item_selection.value.food_name,
            "comment": self.comment_input.value
        })
        self.convert_history_to_pickle()
        #self.history_item_selection.scroll_to_bottom()

    def setup_history_menu(self) -> toga.Box:
        """Setup the history table, that displays previous conversions."""
        history_label = toga.Label("History: ", style=Pack(
            font_family="monospace", font_style="italic"))
        if self.location.is_file():
            data = self.load_history_from_pickle()
        else:
            data = [{"unit_selection": None,
                     "unit_value": None,
                     "density_selection": None,
                     "comment": None}]

        self.history_item_selection = toga.Table(headings=["Unit", "Quantity", "Food Item", "Comment"],
                                                 accessors=[
                                                     "unit_selection", "unit_value", "density_selection", "comment"],
                                                 style=Pack(flex=150),
                                                 multiple_select=False,
                                                 on_select=self.load_history,
                                                 data=data)
        box = toga.Box(children=[  # history_label,
            self.history_item_selection,
                       # toga.Box(children=[load_button, clear_button])
                       ], style=Pack(direction=COLUMN, flex=150))
        return box

    def perform_conversion(self, *kwargs):
        """Convert the current inputs and write history to table."""
        self.write_history()
        # parent conversions
        price = float(self.item_cost_input.value)
        density = (float(self.density_item_selection.value.g_ml)
                   * ureg.gram) / (1 * ureg.ml)
        mass = self.unit_selection.value.mass
        price_per_unit = price/mass
        self.unit.text = round(price_per_unit, 5)

        # Metric Conversions
        # Mass
        self.kg_1.text = round(price/mass.to('kg').m, 5)
        self.g_900.text = round((price/mass.to('gram').m)*900, 5)
        self.g_800.text = round((price/mass.to('gram').m)*800, 5)
        self.g_750.text = round((price/mass.to('gram').m)*750, 5)
        self.g_700.text = round((price/mass.to('gram').m)*700, 5)
        self.g_600.text = round((price/mass.to('gram').m)*600, 5)
        self.g_500.text = round((price/mass.to('gram').m)*500, 5)
        self.g_400.text = round((price/mass.to('gram').m)*400, 5)
        self.g_300.text = round((price/mass.to('gram').m)*300, 5)
        self.g_250.text = round((price/mass.to('gram').m)*250, 5)
        self.g_200.text = round((price/mass.to('gram').m)*200, 5)
        self.g_100.text = round((price/mass.to('gram').m)*100, 5)
        self.g_1.text = round(price/mass.to('gram').m, 5)
        self.mg_1.text = round(price/mass.to('milligram').m, 10)
        # Volume
        self.l_1.text = round(price/(mass/density).to('liter').m, 5)
        self.ml_900.text = round(
            price/(mass/density).to('milliliter').m*900, 5)
        self.ml_700.text = round(
            price/(mass/density).to('milliliter').m*700, 5)
        self.ml_500.text = round(
            price/(mass/density).to('milliliter').m*500, 5)
        self.ml_300.text = round(
            price/(mass/density).to('milliliter').m*300, 5)
        self.ml_100.text = round(
            price/(mass/density).to('milliliter').m*100, 5)

        # Imperi.mal Conversions
        # Mass
        self.lb_3.text = round((price/mass.to('lbs')).m*3, 5)
        self.lb_1.text = round(price/mass.to('lbs').m, 5)
        self.oz_12.text = round((price/mass.to('oz')).m*12, 5)
        self.oz_8.text = round((price/mass.to('oz')).m*8, 5)
        self.oz_6.text = round((price/mass.to('oz')).m*6, 5)
        self.oz_4.text = round((price/mass.to('oz')).m*4, 5)
        self.oz_2.text = round((price/mass.to('oz')).m*2, 5)
        self.oz_1.text = round(price/mass.to('oz').m, 5)
        # Volume
        self.gal_1.text = round(price/(mass/density).to('gallon').m, 5)
        self.gal_half.text = round(price/(mass/density).to('gallon').m*.5, 5)
        self.quart_1.text = round(price/(mass/density).to('quart').m, 5)
        self.pint_1.text = round(price/(mass/density).to('pint').m, 5)
        self.ozf_1.text = round(price/(mass/density).to('fluid_ounce').m, 5)
        self.cup_1.text = round(price/(mass/density).to('cup').m, 5)

        print(type(price_per_unit))
        self.clear_button.style.visibility = 'visible'

        return price_per_unit

    def clean_menu_items(self) -> None:
        """Reset items in menu to an empty text string."""
        self.unit.text = ""
        self.kg_1.text = ""
        self.g_900.text = ""
        self.g_800.text = ""
        self.g_750.text = ""
        self.g_700.text = ""
        self.g_600.text = ""
        self.g_500.text = ""
        self.g_400.text = ""
        self.g_300.text = ""
        self.g_250.text = ""
        self.g_200.text = ""
        self.g_100.text = ""
        self.g_1.text = ""
        self.mg_1.text = ""
        self.l_1.text = ""
        self.ml_900.text = ""
        self.ml_700.text = ""
        self.ml_500.text = ""
        self.ml_300.text = ""
        self.ml_100.text = ""
        self.lb_3.text = ""
        self.lb_1.text = ""
        self.oz_12.text =""
        self.oz_8.text = ""
        self.oz_6.text = ""
        self.oz_4.text = ""
        self.oz_2.text = ""
        self.oz_1.text = ""        
        self.gal_1.text = ""
        self.gal_half.text = ""
        self.quart_1.text = ""
        self.pint_1.text = ""
        self.ozf_1.text = ""
        self.cup_1.text = ""        

    def spawn_menu_items(self) -> None:
        """Create new items in the menu."""
        for object in self.object_spawn_pool:
            setattr(self, object, toga.Label("", style=text_style))
            unit_name = ureg(object.split('_')[0]) * object.split('_')[1]
            setattr(self, object + '_label',
                    toga.Label(f"Price per {unit_name}:", style=text_style))

    def startup(self) -> None:
        self.define_local_data()
        # Define Metric Mass Labels and Layout
        unit_label = toga.Label("Price per unit: ", style=Pack(
            font_family="monospace", font_style="italic"))

        self.object_spawn_pool = ["kg_1", "g_900", "g_800", "g_750", "g_700", "g_600", "g_500", "g_400", "g_300", "g_250", "g_200", "g_100", "g_1", "mg_1", "lb_3", "lb_1", "oz_12", "oz_8", "oz_6",
                             "oz_4", "oz_2", "oz_1", "l_1", "ml_900", "ml_700", "ml_500", "ml_300", "ml_100", "gal_1", "gal_half", "quart_1", "pint_1", "ozf_1", "cup_1"]

        # create menu items
        self.spawn_menu_items()

        self.unit = toga.Label("", style=Pack(
            font_family="monospace", font_style="italic"))

        metric_mass = toga.Box(style=Pack(direction=COLUMN, padding=5), children=[toga.Box(children=[self.kg_1_label, self.kg_1]),
                                                                                  toga.Box(
                                                                                      children=[self.g_900_label, self.g_900]),
                                                                                  toga.Box(
                                                                                      children=[self.g_800_label, self.g_800]),
                                                                                  toga.Box(
                                                                                      children=[self.g_750_label, self.g_750]),
                                                                                  toga.Box(
                                                                                      children=[self.g_700_label, self.g_700]),
                                                                                  toga.Box(
                                                                                      children=[self.g_600_label, self.g_600]),
                                                                                  toga.Box(
                                                                                      children=[self.g_500_label, self.g_500]),
                                                                                  toga.Box(
                                                                                      children=[self.g_400_label, self.g_400]),
                                                                                  toga.Box(
                                                                                      children=[self.g_300_label, self.g_300]),
                                                                                  toga.Box(
                                                                                      children=[self.g_200_label, self.g_200]),
                                                                                  toga.Box(
                                                                                      children=[self.g_250_label, self.g_250]),
                                                                                  toga.Box(
                                                                                      children=[self.g_100_label, self.g_100]),
                                                                                  toga.Box(
                                                                                      children=[self.g_1_label, self.g_1]),
                                                                                  toga.Box(
                                                                                      children=[self.mg_1_label, self.mg_1]),
                                                                                  ])

        imperial_mass = toga.Box(style=Pack(direction=COLUMN, padding=5), children=[toga.Box(children=[self.lb_3_label, self.lb_3]),
                                                                                    toga.Box(
                                                                                        children=[self.lb_1_label, self.lb_1]),
                                                                                    toga.Box(
                                                                                        children=[self.oz_12_label, self.oz_12]),
                                                                                    toga.Box(
                                                                                        children=[self.oz_8_label, self.oz_8]),
                                                                                    toga.Box(
                                                                                        children=[self.oz_6_label, self.oz_6]),
                                                                                    toga.Box(
                                                                                        children=[self.oz_4_label, self.oz_4]),
                                                                                    toga.Box(
                                                                                        children=[self.oz_2_label, self.oz_2]),
                                                                                    toga.Box(
                                                                                        children=[self.oz_1_label, self.oz_1])
                                                                                    ])

        metric_volume = toga.Box(style=Pack(direction=COLUMN, padding=5), children=[
            toga.Box(children=[self.l_1_label, self.l_1]),
            toga.Box(children=[self.ml_900_label, self.ml_900]),
            toga.Box(children=[self.ml_700_label, self.ml_700]),
            toga.Box(children=[self.ml_500_label, self.ml_500]),
            toga.Box(children=[self.ml_300_label, self.ml_300]),
            toga.Box(children=[self.ml_100_label, self.ml_100])
        ])

        imperial_volume = toga.Box(style=Pack(direction=COLUMN, padding=5), children=[
            toga.Box(children=[self.gal_1_label, self.gal_1]),
            toga.Box(children=[self.gal_half_label, self.gal_half]),
            toga.Box(children=[self.quart_1_label, self.quart_1]),
            toga.Box(children=[self.pint_1_label, self.pint_1]),
            toga.Box(children=[self.ozf_1_label, self.ozf_1]),
            toga.Box(children=[self.cup_1_label, self.cup_1])
        ])

        # Define Item Selection
        item_selection_label = toga.Label("Food Item: ", style=text_style)
        self.food_items = read_food_density()
        self.density_item_selection = toga.Selection(items=self.food_items, accessor="food_name", style=Pack(
            padding=(0, 5), flex=50))
        food_dropdown = toga.Box(
            children=[item_selection_label, self.density_item_selection])

        # main menu
        mass_icon = r"resources/mass.png"
        volume_icon = r"resources/volume.png"
        clear_icon = r"resources/clear.png"
        # history_icon = r"resources/history.png"
        warning_icon = r"resources/warning.png"
        option_box = toga.OptionContainer(style=Pack(flex=400),
                                          content=[
            toga.OptionItem("Metric Mass", metric_mass, icon=mass_icon),
            toga.OptionItem("American Mass", imperial_mass, icon=mass_icon),
            toga.OptionItem("Metric Volume", metric_volume, icon=volume_icon),
            toga.OptionItem("American Volume",
                            imperial_volume, icon=volume_icon),
        ])
        item_cost_input_label = toga.Label("Item Cost: ", style=text_style)
        self.item_cost_input = toga.NumberInput(min=0, value=1, step=0.01, style=text_style)
        comment_input_label = toga.Label(
            "Conversion Comment:", style=text_style)
        self.comment_input = toga.TextInput(style=text_style)
        self.comment_input.style.flex = 200
        comment_box = toga.Box(
            children=[comment_input_label, self.comment_input])
        self.unit_selection = toga.Selection(
            items=selection_list, accessor="name", style=Pack(padding=(0, 5), flex=50))

        convert_button = toga.Button("Convert",
                                     on_press=self.perform_conversion,
                                     style=button_style)
        self.clear_button = toga.Button(icon=clear_icon,
                                        on_press=self.reset_input,
                                        style=button_style)
        self.clear_button.style.width = 75        
        self.clear_button.style.visibility = 'hidden'
        clear_convert_box = toga.Box(children=[convert_button, self.clear_button])
        input_form = toga.Box(style=Pack(direction=ROW, flex=25), children=[
                              item_cost_input_label, self.item_cost_input, self.unit_selection])
        ppu = toga.Box(style=Pack(direction=COLUMN, alignment="center"), children=[
                       toga.Box(children=[unit_label, self.unit])])

        # setup main screen layout
        main_box = toga.Box(style=Pack(direction=COLUMN), children=[input_form,
                                                                    food_dropdown,
                                                                    comment_box,
                                                                    toga.Divider(),
                                                                    clear_convert_box,
                                                                    toga.Divider(),
                                                                    ppu,
                                                                    toga.Divider(),
                                                                    option_box,
                                                                    toga.Divider(),
                                                                    self.setup_history_menu()])
        # Add objects to main window
        self.main_window = toga.MainWindow(title="Food Price Comparison",
                                           size=(1024, 1024))
        self.main_window.content = main_box
        clear_history_command = toga.Command(self.clear_history,
                                             text="Clear Conversion History",
                                             icon=warning_icon,
                                             group=toga.Group.EDIT)
        clear_input_command = toga.Command(self.reset_input,
                                           text="Clear Input",
                                           icon=warning_icon,
                                           group=toga.Group.EDIT)
        self.commands.add(clear_history_command)
        self.commands.add(clear_input_command)
        if current_platform == "android":
            export_data_command = toga.Command(self.export_data,
                                           text='Export History',
                                           icon=warning_icon,
                                           group=toga.Group.FILE)
            import_data_command = toga.Command(self.import_data,
                                           text='Import History',
                                           icon=warning_icon,
                                           group=toga.Group.FILE)
            self.commands.add(import_data_command)
            self.commands.add(export_data_command)


def main():
    return main_app(formal_name,
                    full_name,
                    icon="resources/quickfoodpricecomparison.ico")


if __name__ == "__main__":
    main().main_loop()
