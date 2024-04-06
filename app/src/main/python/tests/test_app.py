from src.quickfoodpricecomparison.app import main_app, full_name, formal_name, read_food_density, selection_list, text_style, button_style
from pathlib import Path
from pint import UnitRegistry
from toga.style import Pack


formal_name_test = "Quick Food Price Comparison"
full_name_test = "com.drmantistobbogan.foodpricecomparison"
object = main_app(formal_name_test, full_name)

def test_app_info():
    """Check that app details are correct"""
    assert formal_name == formal_name_test
    assert full_name == full_name_test

def test_local_path():
    """Validate that the local path is working as expected."""
    object.define_local_data()
    assert object.location == Path(str(object.paths.data) + '\conversion_history.pickle')

def test_food_values():
    """Validate that the food list is correct."""
    assert read_food_density()[0] == dict({'food_name': 'alcohol, ethyl', 'g_ml': '0.789', 'specific_gravity': '', 'biblio_id': 'TB', 'category': 'Beverages, alcoholic'})
    assert len(read_food_density())==534
    
def test_selection_list():
    """Check to make sure unit selection list is valid"""
    ureg = UnitRegistry()
    assert selection_list[2]['mass'] == ureg.gram*750
    assert selection_list[9]['mass'] == ureg.ounce*12
    assert len(selection_list)==15

def test_reusable_styles():
    """Test to see that the default styles are setup correctly"""
    assert text_style._PROPERTIES == Pack(padding=(0, 5), font_size=14)._PROPERTIES
    assert button_style._PROPERTIES == Pack(padding=5, font_size=14, flex=150)._PROPERTIES
    
