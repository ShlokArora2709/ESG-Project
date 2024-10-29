import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import itertools
import os
flag = [0]
import string

def generate_combinations():
    # Generate combinations for two letters (AA to ZZ)
    two_letter_combinations = [''.join(i) for i in itertools.product(string.ascii_uppercase, repeat=2)]
    
    return two_letter_combinations[two_letter_combinations.index("WA"):]



options = Options()
options.set_preference("Profile", "/home/shlok/snap/firefox/common/.mozilla/firefox/57sjbxma.default")
driver = webdriver.Firefox(options=options)
driver.get("https://www.msci.com/our-solutions/esg-investing/esg-ratings-climate-search-tool")

# Wait for the page to load
time.sleep(3)  # Adjust if needed

def handle_popup():
    """Fill out and submit the popup dialog if it appears."""
    try:
        driver.switch_to.frame(driver.find_element(By.ID, "_esgratingsprofile_subscriptionFormPopup_iframe_"))
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "_esgratingsprofile_firstName"))
        )
        driver.find_element(By.ID, "_esgratingsprofile_firstName").send_keys("John")
        driver.find_element(By.ID, "_esgratingsprofile_lastName").send_keys("Doe")
        driver.find_element(By.ID, "_esgratingsprofile_jobTitle").send_keys("Analyst")
        driver.find_element(By.ID, "_esgratingsprofile_email").send_keys("johndoe@vips.edu")
        driver.find_element(By.ID, "_esgratingsprofile_company").send_keys("Example Corp")
        
        Select(driver.find_element(By.ID, "_esgratingsprofile_CliCS_Segment")).select_by_index(1)
        Select(driver.find_element(By.ID, "_esgratingsprofile_Primary_Area_Of_Interest")).select_by_index(1)
        Select(driver.find_element(By.ID, "_esgratingsprofile_country")).select_by_index(1)
        
        checkbox = driver.find_element(By.ID, "_esgratingsprofile_acknowledgePrivacyNotice")
        driver.execute_script("arguments[0].click();", checkbox)
        
        submit_button = driver.find_element(By.ID, "_esgratingsprofile_submitButton")
        driver.execute_script("arguments[0].click();", submit_button)

        WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, "_esgratingsprofile_subscriptionFormPopup_iframe_")))
        time.sleep(10)
        flag[0] = 1
        driver.switch_to.default_content()
    except Exception as e:
        print("Popup did not appear")

existing_companies = set()
csv_filename = 'esg_data.csv'

if os.path.exists(csv_filename):
    with open(csv_filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            existing_companies.add(row[0])

# Open CSV file for writing
with open('esg_data.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    if not os.path.getsize(csv_filename):
        writer.writerow(["Company Name", "ESG Rating"])

    # Loop through each combination
    for search_term in generate_combinations():
        search_bar = driver.find_element(By.ID, "_esgratingsprofile_keywords")
        search_bar.clear()
        search_bar.send_keys(search_term)
        num_elements=0
        time.sleep(2.5)
        
        try:
            dropdown = driver.find_element(By.ID, "ui-id-1")
            time.sleep(0.5)
            options_list = dropdown.find_elements(By.TAG_NAME, "li")
            num_elements = len(options_list)
            print(num_elements)
            
            for i in range(num_elements):
                search_bar = driver.find_element(By.ID, "_esgratingsprofile_keywords")
                search_bar.clear()
                search_bar.send_keys(search_term)
                time.sleep(2)

                for _ in range(i + 1):
                    search_bar.send_keys(Keys.ARROW_DOWN)
                    time.sleep(0.25)
                
                search_bar.send_keys(Keys.ENTER)
                time.sleep(3)

                if flag[0] == 0:
                    handle_popup()

                page_source = driver.page_source
                soup = BeautifulSoup(page_source, "html.parser")
                
                header_title = soup.find("h1", class_="header-company-title")
                if header_title:
                    company_name = header_title.get_text(strip=True)
                    if company_name in existing_companies:
                        print(f"Company {company_name} already exists in CSV. Skipping...")
                        continue 
                    print(f"Company Name: {company_name}")

                    driver.find_element(By.ID, "esg-transparency-toggle-link").click()
                    time.sleep(1)

                    page_source = driver.page_source
                    soup = BeautifulSoup(page_source, "html.parser")
                    elements = soup.find_all("g", class_="highcharts-label highcharts-data-label highcharts-data-label-color-undefined")

                    if elements:
                        last_element = elements[-1]
                        esg_rating = last_element.get_text(strip=True)
                        print(f"ESG Rating: {esg_rating}")

                        # Write the data to CSV
                        writer.writerow([company_name, esg_rating])
                        existing_companies.add(company_name)
                    else:
                        print("No ESG Rating found.")

                search_bar = driver.find_element(By.ID, "_esgratingsprofile_keywords")
        except Exception as e:
            print(f"No results found for {search_term}: {e}")

# Close the driver after completion
driver.quit()
