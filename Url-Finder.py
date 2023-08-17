import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
import pandas as pd
import os.path

# List of companies
companies = [
    "GESTORE DEI MERCATI ENERGETICI",
    "ENI",
    "STELLANTIS EUROPE",
    "Ferrari automobili",
    "Universita Milano Bicocca"
    # ... (add all other companies here)
]

# File path for the Excel file
excel_file_path = 'Url-Finder.xlsx'

# Start the webdriver
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())  # starts the webdriver

# Create a list to store company data
company_data = []

# Check if the Excel file exists
if os.path.exists(excel_file_path):
    # Load existing data from the Excel file
    existing_df = pd.read_excel(excel_file_path)
    company_data.extend(existing_df.to_dict(orient='records'))

# Iterate through the list of companies
for company in companies:
    # Open DuckDuckGo search page
    driver.get("https://www.duckduckgo.com")

    # Find the search bar and type in the company name
    search_bar = driver.find_element(By.NAME, "q")
    search_bar.send_keys(company)
    search_bar.send_keys(Keys.RETURN)

    # Wait for search results to load
    time.sleep(3)
    
    # Find the span containing "https"
    try:
        url_span = driver.find_element(By.XPATH, "//span[contains(text(), 'https')]")
        company_url = url_span.text
    except:
        company_url = "No URL found"
    
    company_data.append({"Company": company, "URL": company_url})
    
    time.sleep(2)  # Delay for 2 seconds before the next search

# Create a DataFrame from the company data
df = pd.DataFrame(company_data)

# Save the DataFrame to the Excel file
df.to_excel(excel_file_path, index=False)

# Close the browser
driver.quit()
