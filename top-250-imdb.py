from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set up Selenium with a headless Chrome browser
options = Options()
# options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

# Navigate to the IMDb Top 250 page
driver.get("https://www.imdb.com/chart/top")
time.sleep(3)  # Allow time for JavaScript to load the full page content

# Get the page source and pass it to BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Close the driver
driver.quit()

# Extract titles and positions
titlesls = []
positions = []
titles = soup.find_all('h3', class_='ipc-title__text')
for title in titles:
    title_text = title.text.strip()
    if ". " in title_text:
        rank, movie_name = title_text.split(". ", 1)
        positions.append(int(rank))
        titlesls.append(movie_name.strip())

# Extract years of release
yearsls = []
years = soup.select(
    "div.sc-5bc66c50-5.hVarDB.cli-title-metadata > span:nth-child(1)")
for year in years:
    year_text = year.text.strip()
    yearsls.append(int(year_text))

# Zip the data into a DataFrame with position, title, year
Data = list(zip(positions, titlesls, yearsls))
df = pd.DataFrame(data=Data, columns=[
                  'Position', 'Name', 'Year'])

timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

# File path for the CSV
file_path = 'top-250-movies.csv'

# Write the timestamp and then the DataFrame to the CSV
with open(file_path, 'w') as f:
    # Write timestamp as a comment
    f.write(f"# Data scraped on: {timestamp}\n")
# Append DataFrame without overwriting
df.to_csv(file_path, mode='a', index=False, header=True)
