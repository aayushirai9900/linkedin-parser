# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 17:15:55 2022

@author: pavankumar.alluri
"""

# import web driver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
# Removes duplicates from list, while preserving the order
def rem_dup(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

# Find indices of Endorsement
def find_ind(my_list):
    return [i for i, s in enumerate(my_list) if 'endorsement' in s]

def get_linkedin_skills(link):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')

    # chromedirver installation
    driver = webdriver.Chrome(ChromeDriverManager().install() ,options=option)
    # driver.get method() will navigate to a page given by the URL address
    driver.get('https://www.linkedin.com/uas/login?fromSignIn=true&trk=cold_join_sign_in')
    # locate email form by_class_name and send keys
    username = driver.find_element(By.ID,'username')
    username.send_keys('aayushirai9900@gmail.com')#enter your email id associated with linkedin here
    # locate password form by_class_name and send keys
    password = driver.find_element(By.ID,'password')
    password.send_keys('5121@@@@')#enter your linkedin password here
    sleep(2)
    # locate submit button by_class_name and click
    driver.find_element(By.CLASS_NAME,'login__form_action_container  ').click()
    #print(driver.find_element(By.CLASS_NAME,'login__form_action_container  ').click())
    #sleep(3)

    driver.get(link)#'https://www.linkedin.com/in/guna-venkat-doddi/details/skills/')
    #sleep(2)
    driver.execute_script("document.body.style.zoom='25%'")
    #print(driver.get(link) )
    #sleep(2)
    All_Skills = []
    try:
        AS = driver.find_elements(By.XPATH,'//div[@class="artdeco-tabpanel active ember-view"]') 
        for i in AS:
            All_Skills.append(i.text)
    except:
        All_Skills.append("No SKills on LinkedIn")
    #print(All_Skills)    
    All_Skills = All_Skills[0].split('\n')
    All_Skills = All_Skills[1::2]
    All_Skills = [x for x in All_Skills if not 'Passed LinkedIn Skill Assessment' in x]
    All_Skills = [x for x in All_Skills if not ' at' in x]
    All_Skills = [x for x in All_Skills if not 'Endorsed' in x]
    All_Skills = [x for x in All_Skills if not 'Show more results' in x]
    Ind = find_ind(All_Skills)

    Endor_Skills = []
    To_remove = []
    for i in range(len(Ind)):
        Endor_Skills.append(All_Skills[Ind[i]-1:Ind[i]+1])
        To_remove.append(Endor_Skills[i][0])

    a = [x for x in All_Skills if not 'endorsement' in x]
    b = [i for i in a if i not in To_remove]

    for i in b: Endor_Skills.append(i)

    skills_df = pd.DataFrame()
    skills_df['Skills'] = Endor_Skills
    # print(skills_df)
    driver.close()
    return skills_df
#print(get_linkedin_skills('https://www.linkedin.com/in/guna-venkat-doddi/details/skills/'))

