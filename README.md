# NBA Players statistics
## A fun personal project.

This is a fun project I created to visualize some statistics of NBA players in the current season, after learning some Selenium and Python Dash.

Feel free to clone this repo and have a play about. You can recreate the environment using conda by opening a terminal in the cloned project and typing

```
conda env create -f nba_env.yml
```

The file ```nba_players.csv ``` contains data scraped from the Advanced Statistics page of NBA.com. To re-scrape the page, activate the conda enviroment in the terminal and enter ```python nba_selenium.py```. After about 30 seconds, the data will have been rescraped, reflecting the current statistics for the season.

To activate the little visualization applet, activate the conda environment (if not done already) and enter into the terminal ```python app.py```. Then open your web browser and navigate to ```localhost:8050```.

Cheers!