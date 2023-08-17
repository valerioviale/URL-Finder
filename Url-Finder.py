import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
import pandas as pd
import os.path

# List of companies
companies = [
    "	SEND TO ME S.R.L.	"	,
"	GUCCI LOGISTICA SOCIETA' PER AZIONI	"	,
"	GOTTARDO S.P.A.	"	,
"	BOLTON FOOD S.P.A.	"	,
"	GENERAL CAVI - SOCIETA' PER AZIONI	"	,
"	G.A. OPERATIONS S.P.A.	"	,
"	HAVI LOGISTICS S.R.L.	"	,
"	WUERTH S.R.L. - G.M.B.H.	"	
    # ... (add all other companies here)
]

# File path for the Excel file
excel_file_path = 'Url-Finder.xlsx'

# Domains to exclude
excluded_domains = ["wikipedia.org", "www.dnb.com", "it.kompass.com","gb.kompass.com", "www.ufficiocamerale.it", "it.linkedin.com", "www.linkedin.com", "www.bloomberg.com","www.informazione-aziende.it", "atoka.io", "www.reportaziende.it", "www.europages.co.uk", "italy.globaldatabase.com", "www.creditsafe.com","creditsafe.com", "registroaziende.it", "www.icribis.com", "www.gdonews.it", "www.visura.pro", "www.gdoweek.it", "www.empresite.it", "www.paginebianche.it",".linkedin.com", "www.companyreports.it"]

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
    time.sleep(2)
    
    # Find all spans containing "https"
    url_spans = driver.find_elements(By.XPATH, "//span[contains(text(), 'https')]")
    
    company_url = "No URL found"
    
    for url_span in url_spans:
        url = url_span.text
        excluded = False
        for domain in excluded_domains:
            if domain in url:
                excluded = True
                break
        
        if excluded:
            # Skip excluded URLs and move to the next URL
            continue
        
        company_url = url
        break  # Stop searching once a valid URL is found
    
    company_data.append({"Company": company, "URL": company_url})
    
    time.sleep(1)  # Delay for 2 seconds before the next search

# Create a DataFrame from the company data
df = pd.DataFrame(company_data)

# Save the DataFrame to the Excel file
df.to_excel(excel_file_path, index=False)

# Close the browser
driver.quit()
