# Description
The goal of this app is to perform a very straight forward comparison of a price per unit for one item to a price per unit of another item.

## Features
- Convert between metric units and American imperial units.</li>
- Get an estimate of price per volume for about 500 different product types.</li>
- Save a history of your conversions for accessing later.</li>

# Building
This project is built with [Beeware](https://github.com/beeware) and [Python](https://www.python.org/downloads/release/python-31014/).

To generate the files required using Beeware natively:
1. Clone this [repository](https://github.com/DrMantisTobbogan/foodpricecomparison/tree/master).
2. Setup a Python 3.10 venv or conda environment.
3. Install the requirments using `pip install -r requirements.txt.`
4. In a terminal session, run `briefcase build android` to build a debug APK.
5. Once ready, in a terminal session run `briefcase package android` to build the aab file.
6. Sign the .aab file using `jarsigner.exe -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore "C:\Users\user_name\.android\quick-food-price-comparison.jks" "D:\quickfoodpricecomparison\dist\Quick Food Price Comparison-X.X.X.aab" upload-key -storepass android`

# Credits
Huge shout-out to the Beeware project team, their project is really good for a small rainy day project like this.

 