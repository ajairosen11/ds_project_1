from selenium.webdriver.chrome.service import Service
import pandas as pd
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from config import email_pw
from selenium.webdriver.common.keys import Keys
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_data(job_title, no_of_pages):
    service = Service(executable_path='chromedriver.exe')
    driver = uc.Chrome(service=service)
    url = 'https://www.glassdoor.co.in/index.htm'
    driver.get(url)
    
    # Wait for the email input field to be clickable
    email_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "inlineUserEmail")))
    email_input.send_keys('vishalajairosen@gmail.com')
    
    # Wait for the continue with email button to be clickable
    continue_with_email_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "css-1h52dri")))
    continue_with_email_button.click()
    
    # Wait for the password input field to be clickable
    password_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "inlineUserPassword")))
    password_input.send_keys(email_pw)
    
    # Wait for the sign-in button to be clickable
    sign_in_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "gd-ui-button")))
    sign_in_button.click()
    
    # Wait for the jobs link to be clickable
    jobs_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Jobs")))
    jobs_link.click()
    
    search_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "searchBar-jobTitle")))
    search_input.send_keys(job_title)
    search_input.send_keys(Keys.RETURN)
    
    svg_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="SVGInline-svg modal_closeIcon-svg"]')))
    svg_element.click()

    lst = []
    for j in range(3, no_of_pages + 5):
        print('The Scraping Page Number: ', j - 2)
        for i in range(1, 31):
            t = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="MainCol"]/div[1]/ul/li[{}]/div/div/a'.format(i))))
            lst.append(t.text)
        next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="MainCol"]/div[2]/div/div[1]/button[{}]'.format(j))))
        next_button.click()

    split_data = [item.split('\n') for item in lst]

    def split_names_digits(item):
        match = re.search(r'([A-Za-z\s]+)(\d+\.\d+)\s★', item)
        if match:
            return [match.group(1), match.group(2)]
        else:
            return [item, 'Nil']

    for inner_list in split_data:
        inner_list[:1] = split_names_digits(inner_list[0])

    for inner_list in split_data:
        if len(inner_list) == 5:
            inner_list.insert(4, 'Nil')
        if len(inner_list) == 7 and inner_list[5] == 'Easy Apply':
            inner_list.pop(5)

    df = pd.DataFrame(split_data, columns=['Company', 'Rating', 'Job_Role', 'Location', 'Salary_Range', 'Posted_Time'])

    return df
