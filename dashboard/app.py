
from shiny import reactive, render
from shiny.express import input, ui
from shinyswatch import theme
from shinywidgets import render_plotly
import random
from datetime import datetime
from collections import deque
import pandas as pd
import plotly.express as px
from scipy import stats
from faicons import icon_svg

# --------------------------------------------
# Shiny EXPRESS VERSION
# --------------------------------------------

# --------------------------------------------
# First, set a constant UPDATE INTERVAL for all live data
# Constants are usually defined in uppercase letters
# Use a type hint to make it clear that it's an integer (: int)
# --------------------------------------------

UPDATE_INTERVAL_SECS: int = 5

# --------------------------------------------
# Initialize a REACTIVE VALUE with a common data structure
# The reactive value is used to store state (information)
# Used by all the display components that show this live data.
# This reactive value is a wrapper around a DEQUE of readings
# --------------------------------------------

DEQUE_SIZE: int = 8
reactive_value_wrapper = reactive.value(deque(maxlen=DEQUE_SIZE))


ui.page_opts(title="Kamalini's PyShiny Live Data", fillable=True)

theme.cosmo()

with ui.sidebar(open="open"):

    ui.h2("Maryville Temperature", class_="text-center")
    ui.p(
        "A demonstration of real-time temperature readings in Maryville, Missouri.",
        class_="text-center",
    )
    ui.hr()
    ui.input_numeric("temp_low", "Lowest Temperature", 30)
    ui.input_numeric("temp_high", "Highest Temperature", 75)
    ui.h6("Links:")
    ui.a(
        "GitHub Source",
        href="https://github.com/S573647/cintel-05-cintel",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://github.com/S573647/cintel-05-cintel",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "PyShiny Express",
        href="https://shiny.posit.co/blog/posts/shiny-express/",
        target="_blank",
    )


@reactive.calc()
def reactive_calc_combined():
    # Invalidate this calculation every UPDATE_INTERVAL_SECS to trigger updates
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)

    # Data generation logi
    temp = round(random.uniform(input.temp_low(), input.temp_high()), 1)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_dictionary_entry = {"temp":temp, "timestamp":timestamp}

    # get the deque and append the new entry
    reactive_value_wrapper.get().append(new_dictionary_entry)

    # Get a snapshot of the current deque for any further processing
    deque_snapshot = reactive_value_wrapper.get()

    # For Display: Convert deque to DataFrame for display
    df = pd.DataFrame(deque_snapshot)

    # For Display: Get the latest dictionary entry
    latest_dictionary_entry = new_dictionary_entry

    # Return a tuple with everything we need
    # Every time we call this function, we'll get all these values
    return deque_snapshot, df, latest_dictionary_entry


# In Shiny Express, everything not in the sidebar is in the main panel

with ui.layout_columns():
    with ui.value_box(
        showcase=icon_svg("sun"),
        theme="bg-gradient-blue-purple",
    ):

        "Current Temperature"

        @render.text
        def display_temp():
            """Get the latest reading and return a temperature string"""
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['temp']} F"

        "Mostly Sunny"

  
    with ui.card(full_screen=True, style="background-color: lavender"):
        ui.card_header("Current Date and Time")

        @render.text
        def display_time():
            """Get the latest reading and return a timestamp string"""
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            return f"{latest_dictionary_entry['timestamp']}"


with ui.layout_columns(col_widths=(4, 8)): # Making each card a different width
    with ui.card(full_screen=True, style="background-color: lavender"):
        ui.card_header("Most Recent Readings")

        @render.data_frame
        def display_df():
            """Get the latest reading and return a dataframe with current readings"""
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            pd.set_option('display.width', None)        # Use maximum width
            return render.DataGrid( df,width="100%")

    with ui.card(full_screen=True, style="background-color: lavender"):
        ui.card_header("Chart with Current Trend")

        @render_plotly
        def display_plot():
            # Fetch from the reactive calc function
            deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()

            # Ensure the DataFrame is not empty before plotting
            if not df.empty:
                # Convert the 'timestamp' column to datetime for better plotting
                df["timestamp"] = pd.to_datetime(df["timestamp"])

                # Create scatter plot for readings
                # pass in the df, the name of the x column, the name of the y column,
                # and more
            
                fig = px.scatter(df,
                x="timestamp",
                y="temp",
                title="Temperature Readings with Regression Line",
                labels={"temp": "Temperature (°F)", "timestamp": "Time"},
                color_discrete_sequence=["Black"] )
                
                # Linear regression - we need to get a list of the
                # Independent variable x values (time) and the
                # Dependent variable y values (temp)
                # then, it's pretty easy using scipy.stats.linregress()

                # For x let's generate a sequence of integers from 0 to len(df)
                sequence = range(len(df))
                x_vals = list(sequence)
                y_vals = df["temp"]

                slope, intercept, r_value, p_value, std_err = stats.linregress(x_vals, y_vals)
                df['best_fit_line'] = [slope * x + intercept for x in x_vals]

                # Add the regression line to the figure
                fig.add_scatter(x=df["timestamp"], y=df['best_fit_line'], mode='lines', name='Regression Line')

                # Update layout as needed to customize further
                fig.update_layout(xaxis_title="Time",yaxis_title="Temperature (°F)")

            return fig