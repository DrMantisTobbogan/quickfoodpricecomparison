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
import csv
import pickle
import pkg_resources
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
    ''''''    
    # Specify the path to your CSV file
    if current_platform == "android":
        csv_file_path = pkg_resources.resource_filename(__name__, 'food_density.csv')
    else:
        csv_file_path = r"D:\python_workspace\quickfoodpricecomparison\src\quickfoodpricecomparison\food_density.csv"
    csv_data = []

    # Open the CSV file and read its contents
    with open(csv_file_path, "r", encoding='utf-8-sig') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            csv_data.append(row)
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

            bytesJarray = bytes(
                (context.getContentResolver().openInputStream(data).readAllBytes()))
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
            # input_stream.close()
            output_stream.close()

            print(f'Saved {byte_count} bytes to {uri.toString()}')
        else:
            pass
    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

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
        # self.history_item_selection.scroll_to_bottom()

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

        for object in self.object_spawn_pool:
            unit, value = self.get_spawned_unit_and_value(object)
            if unit in ['kg', 'g', 'mg', 'lbs', 'oz']:
                getattr(self, object).text = round(
                    price/mass.to(unit).m * float(value), 5)
            elif unit in ['l', 'ml', 'gallon', 'quart', 'pint', 'fluid_ounce', 'cup']:
                getattr(self, object).text = round(
                    price/(mass/density).to(unit).m * float(value), 5)
        print(type(price_per_unit))
        self.clear_button.style.visibility = 'visible'

        return price_per_unit

    def clean_menu_items(self) -> None:
        """Reset items in menu to an empty text string."""
        for attr in self.object_spawn_pool:
            getattr(self, attr).text = ""

    def get_spawned_unit_and_value(self, object: str) -> tuple[str, float]:
        """Parse the current object from the spawn pool and return it's unit string and value"""
        unit = object.split('_')[0]
        value = object.split('_')[1]
        if unit == "fluidounce":
            unit = "fluid_ounce"
        if value == "half":
            value = 0.5
        return [unit, float(value)]

    def spawn_menu_items(self) -> None:
        """Create new items in the menu."""
        for object in self.object_spawn_pool:
            setattr(self, object, toga.Label("", style=text_style))
            unit, value = self.get_spawned_unit_and_value(object)
            unit_name = ureg(unit) * value
            setattr(self, object + '_label',
                    toga.Label(f"Price per {unit_name}:", style=text_style))

    def startup(self) -> None:
        self.define_local_data()
        # Define Metric Mass Labels and Layout
        unit_label = toga.Label("Price per unit: ", style=Pack(
            font_family="monospace", font_style="italic"))

        self.object_spawn_pool = ["kg_1", "g_900", "g_800", "g_750", "g_700", "g_600", "g_500", "g_400", "g_300", "g_250", "g_200", "g_100", "g_1", "mg_1", "lbs_3", "lbs_1", "oz_12", "oz_8", "oz_6",
                                  "oz_4", "oz_2", "oz_1", "l_1", "ml_900", "ml_800", "ml_700", "ml_600", "ml_500", "ml_400", "ml_300", "ml_200", "ml_100", "gallon_1", "gallon_half", "quart_1", "pint_1", "fluidounce_1", "cup_1"]

        # create menu items in the conversion screen
        self.spawn_menu_items()
        self.unit = toga.Label("", style=Pack(
            font_family="monospace", font_style="italic"))
        self.metric_mass_children = []
        self.imperial_mass_children = []
        self.metric_volume_children = []
        self.imperial_volume_children = []
        for object in self.object_spawn_pool:
            unit, value = self.get_spawned_unit_and_value(object)
            if unit in ['kg', 'g', 'mg']:
                self.metric_mass_children.append(
                    toga.Box(children=[getattr(self, object + '_label'), getattr(self, object)]))
            elif unit in ['lbs', 'oz']:
                self.imperial_mass_children.append(
                    toga.Box(children=[getattr(self, object + '_label'), getattr(self, object)]))
            elif unit in ['l', 'ml']:
                self.metric_volume_children.append(
                    toga.Box(children=[getattr(self, object + '_label'), getattr(self, object)]))
            elif unit in ['gallon', 'quart', 'pint', 'fluid_ounce', 'cup']:
                self.imperial_volume_children.append(
                    toga.Box(children=[getattr(self, object + '_label'), getattr(self, object)]))
        metric_mass = toga.Box(style=Pack(
            direction=COLUMN, padding=5), children=self.metric_mass_children)
        imperial_mass = toga.Box(style=Pack(
            direction=COLUMN, padding=5), children=self.imperial_mass_children)
        metric_volume = toga.Box(style=Pack(
            direction=COLUMN, padding=5), children=self.metric_volume_children)
        imperial_volume = toga.Box(style=Pack(
            direction=COLUMN, padding=5), children=self.imperial_volume_children)

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
        self.item_cost_input = toga.NumberInput(
            min=0, value=1, step=0.01, style=text_style)
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
        clear_convert_box = toga.Box(
            children=[convert_button, self.clear_button])
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
