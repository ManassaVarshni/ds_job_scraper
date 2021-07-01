# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 19:24:48 2021

@author: MANU
"""

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

#specify driver path
DRIVER_PATH = 'Downloads/chromedriver.exe'
driver = webdriver.Chrome(executable_path = DRIVER_PATH)
# Setting time for driver to look for the the element for 10 seconds before quitting
driver.implicitly_wait(10)

# Specifying the website url to scrape
driver.get('https://indeed.com')

search_job = driver.find_element_by_xpath('//*[@id="text-input-what"]')
search_job.send_keys(['data science'])

search_place = driver.find_element_by_xpath('//*[@id="text-input-where"]')
search_place.send_keys(['india'])

search_button = driver.find_element_by_xpath('//*[@id="whatWhereFormId"]/div[3]/button')
search_button.click()

# Click advance job search for changing 
advance_search_button = driver.find_element_by_xpath('/html/body/table[1]/tbody/tr/td/table/tbody/tr/td/form/table/tbody/tr/td[4]/a')
advance_search_button.click()

#set display limit of 30 results per page
display_limit = driver.find_element_by_xpath('//*[@id="limit"]//option[@value="50"]')
display_limit.click()

#sort by date
#sort_option = driver.find_element_by_xpath('//*[@id="sort"]//option[@value="relevance"]')
#sort_option.click()

search_button = driver.find_element_by_xpath('//*[@id="fj"]')
search_button.click()

# To close pop up window
close_popup = driver.find_element_by_id("popover-x")
close_popup.click()

titles=[]
companies=[]
locations=[]
links =[]
ratings=[]
salaries = []
descriptions=[]

for i in range(0, 200):
    job_card = driver.find_elements_by_xpath('//div[@class="jobsearch-SerpJobCard unifiedRow row result clickcard"]')
    
    for job in job_card:
           
        #  Collecting ratings 
        try:
            rating = job.find_element_by_xpath('.//span[@class="ratingsContent"]').text
        except:
            rating = "None"
        ratings.append(rating)
    
        #  Collecting salary
        try:
            salary = job.find_element_by_xpath('.//span[@class="salaryText"]').text
        except:
            salary = "None"    
        salaries.append(salary)
        
        # Collecting job location
        try:
            location = job.find_element_by_xpath('.//span[@class="location accessible-contrast-color-location"]').text
        except:
            location = "None"      
        locations.append(location)
        
        #  Collecting job title
        try:
            title  = job.find_element_by_xpath('.//h2[@class="title"]//a').text
        except:
            title = job.find_element_by_xpath('.//h2[@class="title"]//a').get_attribute(name="title")
        titles.append(title)
        
        #  Collecting job url
        links.append(job.find_element_by_xpath('.//h2[@class="title"]//a').get_attribute(name="href"))
        
        #  Collecting company name
        companies.append(job.find_element_by_xpath('.//span[@class="company"]').text)
    

descriptions=[]
for link in links:
    
    driver.get(link)
    jd = driver.find_element_by_xpath('//div[@id="jobDescriptionText"]').text
    descriptions.append(jd)
    """
    try:
        next_page = driver.find_element_by_xpath('//a[@aria-label={}]//span[@class="pn"]'.format(i+2))
        next_page.click()

    except:
        next_page = driver.find_element_by_xpath('//a[@aria-label="Next"]//span[@class="np"]')
        next_page.click()
    #except:
        #next_page = driver.find_element_by_xpath('//a[.//span[contains(text(),"Next")]]')
        #next_page.click()
        
    
    print("Page: {}".format(str(i+2)))
    """

df=pd.DataFrame()
df['Title']=titles
df['Company']=companies    
df['Location']=locations
df['Link']=links
df['Rating']=ratings
df['Salary']=salaries
df['Description']=descriptions

df.to_csv(r'F:\Projects\ds_salary_proj\DS_Jobs.csv', index = False)