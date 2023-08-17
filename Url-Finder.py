from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# List of companies
companies = [
    "	GESTORE DEI MERCATI ENERGETICI S.P.A.	"	,
"	ENI S.P.A.	"	,
"	STELLANTIS EUROPE S.P.A.	"	,
"	ENEL GLOBAL TRADING S.P.A.	"	,
"	ENI TRADING & SHIPPING S.P.A.	"	,
"	GESTORE DEI SERVIZI ENERGETICI - GSE S.P.A.	"	,
"	ENEL ENERGIA S.P.A.	"	,
"	ENGIE ITALIA SPA	"	,
"	KUWAIT PETROLEUM ITALIA S.P.A.	"	,
"	TELECOM ITALIA SPA O TIM S.P.A.	"	,
"	AMAZON WEB SERVICES EMEA SARL	"	,
"	ALESSANDRO PATANE' SRL	"	,
"	ESSO ITALIANA S.R.L.	"	

    
    # ... (add all other companies here)
]


# Start the webdriver
#driver = webdriver.Chrome("C:/Users/valerio/Desktop/Courses/LinkedinAuto/chromedriver.exe")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))  # starts the webdriver

# Create a list to store company data
company_data = []

# Iterate through the list of companies
for company in companies:
    # Open Google search page
    driver.get("https://www.google.com")
    
    # Find the search bar and type in the company name
    search_bar = driver.find_element(By.NAME, "q")
    search_bar.send_keys(company)
    search_bar.send_keys(Keys.RETURN)
    
    # Find the first search result (assuming it's the company's official website)
    try:
        result = driver.find_element(By.CSS_SELECTOR, "div.g a")
        company_url = result.get_attribute("href")
        company_data.append({"Company": company, "URL": company_url})
    except:
        company_data.append({"Company": company, "URL": "No URL found"})

# Close the browser
driver.quit()

# Create a DataFrame from the company data
df = pd.DataFrame(company_data)

# Read the existing file into a pandas dataframe
try:
        existing_df = pd.read_excel("URL-finder.xlsx")
        # Concatenate the existing data with the new data
        final_df = pd.concat([existing_df, df], ignore_index=True)
except FileNotFoundError:
        # If the file doesn't exist, just write the new data to it
        final_df = df

    # Write the final data to the same excel file
final_df.to_excel("URL-finder.xlsx", index=False, sheet_name='Sheet1', engine='openpyxl')

