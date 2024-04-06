from shiny import reactive, render, App
from shiny.express import ui
import random
from datetime import datetime
from faicons import icon_svg


UPDATE_INTERVAL_SECS: int = 1


@reactive.calc()
def reactive_calc_combined():
    # Invalidate this calculation every UPDATE_INTERVAL_SECS to trigger updates
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)
        
    # Data generation logic. Get random between -18 and -16 C, rounded to 1 decimal place
    tempinc = round(random.uniform(-18, -5), 1)
    tempinf = round((tempinc*9/5)+32,2)
    

    # Get a timestamp for "now" and use string format strftime() method to format it
    # 
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    latest_dictionary_entry = {"tempinCelsius": tempinc, 
                               "tempinfahrenheit": tempinf,
                               "timestamp": timestamp}

    # Return everything we need
    return latest_dictionary_entry

# ------------------------------------------------
# Define the Shiny UI Page layout - Page Options
# ------------------------------------------------

# Call the ui.page_opts() function
# Set title to a string in quotes that will appear at the top
# Set fillable to True to use the whole page width for the UI

ui.page_opts(title="PyShiny Express: Live Data (Basic)", fillable=True)

with ui.sidebar(open="open"):

    ui.h2("Antarctic Explorer", class_="text-center")

    ui.p(
        "A demonstration of real-time temperature readings in Antarctica.",
        class_="text-center",
    )

    
ui.h2("Current Temperature")

@render.text
def display_temp():
    """Get the latest reading and return a temperature string"""
    latest_dictionary_entry = reactive_calc_combined()
    return f"{latest_dictionary_entry['tempinCelsius']} C, {latest_dictionary_entry['tempinfahrenheit']} F"
    

ui.p("warmer than usual")
icon_svg("sun")


ui.hr()

ui.h2("Current Date and Time")

@render.text
def display_time():
    """Get the latest reading and return a timestamp string"""
    latest_dictionary_entry = reactive_calc_combined()
    return f"{latest_dictionary_entry['timestamp']}"
