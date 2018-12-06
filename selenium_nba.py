from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import numpy as np
import pandas as pd
import sys

def create_browser(start_url):

	o = Options()
	o.add_argument('-private')
	o.headless = True
	#o.add_argument("--headless");

	browser = webdriver.Firefox(options=o)

	browser.get(start_url)

	return browser

sys.stdout.write("Opening Firefox browser...")
url = 'https://stats.nba.com/players/traditional/'
browser = create_browser(url)

# Wait a few seconds before reading the content.
browser.implicitly_wait(5)

# Set the per-mode to totals (option 1 in the list)
browser.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/div[1]/div[3]/div/div/label/select/option[1]').click()

# Show all the entries in the table
browser.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[3]/div/div/select/option[1]').click()

# Get the stats table element from the html
table = browser.find_element_by_class_name('nba-stat-table__overflow')

sys.stdout.write("\nReading data from table...")
# Get all the data from the table in a list, separated by newlien chars
lines = table.text.split('\n')

# Close the browser as it is no longer required.
browser.quit()

N = len(lines)
player_ids = [lines[x] for x in range(N) if x % 3 == 1]
player_names = [lines[x] for x in range(N) if x % 3 == 2]
player_stats = [lines[x].split(' ') for x in range(N) if x % 3 == 0][1:]
col_names = lines[0].split(' ')

import numpy as np
import pandas as pd
T = np.array(player_stats).transpose()
D = {a:b for (a,b) in zip(col_names,[player_names]+list(T))}
df = pd.DataFrame(D)

# Either write the data to SQL database or output to a csv file
to_postgres = True
if to_postgres:
	
	sys.stdout.write("\nWriting to postgres database...")

	# Remove the percent signs from variable names, replace them with Z's
	df.rename(columns={'FT%': 'FTZ', 'FG%': 'FGZ', '3P%':'3PZ'},inplace=True)

	# Write variables in lower case for SQL queries
	df.rename(columns=lambda x: x.lower().strip(),inplace=True)

	TABLE_NAME = "players"
	import nba_db
	with nba_db.db_connect().begin() as conn:
	    df.to_sql(TABLE_NAME, conn, if_exists='replace')

else:
	sys.stdout.write("\nWriting to csv...")
	df.to_csv('nba_players.csv',index=False)

# ALL DONE!
sys.stdout.write("\nDone.\n")
