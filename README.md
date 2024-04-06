# cintel-05-cintel
Basic version for module 5 Live data and continuous Intelligence 
Added faicons for better icons on our cards
used pandas (and pyarrow) for data manipulation
Used shinywidgets for showing plotly charts (render_plotly) and more
Used plotly for interactive charts
Used scipy for statistical analysi

# Run Locally - Initial Start
# commands
py -m venv .venv
.venv\Scripts\Activate
py -m pip install --upgrade pip setuptools
py -m pip install --upgrade -r requirements.txt

# Command to run the Shiny project code 

Add folder dashboard and move the app.py to that folder 
shiny run --reload --launch-browser dashboard/app.py
Open a browser to http://127.0.0.1:8000/ and test the app.

# Export to Docs Folder
shiny static-assets remove
shinylive export dashboard docs
py -m http.server --directory docs --bind localhost 8008
Open a browser to http://[::1]:8008/ and test the Pages app.
