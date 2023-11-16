# pip install selenium
# pip install beautifulsoup4
# pip install webdriver_manager

# using google chrome version 119.0.6045.159, WebDriver isn't avaible yet. 
# 
# Link to download chrome webdriver: https://googlechromelabs.github.io/chrome-for-testing/


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def scrape_hiv_database(url, chromedriver_path):
    options = Options()
    options.headless = True
    options.add_argument('--no-sandbox')  # Add this line

    # Specify the path to ChromeDriver using the executable_path option
    options.add_argument(f"webdriver.chrome.driver={chromedriver_path}")

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(options=options)
    
    # Load the URL
    driver.get(url)

    # Get the page source after waiting for some time to allow dynamic content to load
    driver.implicitly_wait(10)
    page_source = driver.page_source

    # Close the driver
    driver.quit()

    # Parse the HTML content of the page
    soup = BeautifulSoup(page_source, 'html.parser')

    # Update the XPath expression based on your HTML structure
    xpath_expression = "/html/body/div/div[5]/form/table/tbody/tr[1]/td[2]/table/tbody/tr[27]/td[2]"
    days_from_infection_elements = soup.select(xpath_expression)

    # Extract the text content from each element
    days_from_infection_list = [element.get_text() for element in days_from_infection_elements]

    return days_from_infection_list

# URL of the HIV database
url = 'https://www.hiv.lanl.gov/components/sequence/HIV/asearch/map_db.comp'
# Replace 'your_chromedriver_path_here' with the actual path to Chromedriver WHEN THE RIGHT VERSION IS RELEASED 
chromedriver_path = '/Users/laurelrobbins/Documents/chromedriver-mac-arm64'
days_from_infection_data = scrape_hiv_database(url, chromedriver_path)

# Print the list of days from infection
print(days_from_infection_data)

