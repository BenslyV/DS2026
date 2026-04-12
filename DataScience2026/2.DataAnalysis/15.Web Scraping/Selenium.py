from selenium import webdriver
from selenium.webdriver.common.by import By

# Launch Chrome browser
driver = webdriver.Chrome()

# Open a website
driver.get("https://quotes.toscrape.com/")

# Get page title
print("Page Title:", driver.title)

# Close browser
driver.quit()