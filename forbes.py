from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get('https://forbes.com/billionaires') # accesez site-ul principal
driver.implicitly_wait(15)

all = driver.find_elements_by_class_name('table-row')

allInfo = driver.find_elements_by_class_name('expanded-content') # retin toate clasele ascunse

f = open("demofile2.txt", "a")
f.truncate(0)

g = open("demofile3.txt", "a")
g.truncate(0)

def completeList():
    for item in all:
        try:
            rank = item.find_element_by_class_name('rank').text
        except Exception as ex:
            rank = 'NAN'

        try:
            name = item.find_element_by_class_name('personName').text
        except Exception as ex:
            name = 'NAN'
        
        try:
            net = item.find_element_by_class_name('netWorth').text
        except Exception as ex:
            net = 'NAN'

        try:
            age = item.find_element_by_class_name('age').text
        except Exception as ex:
            age = 'NAN'

        try:
            country = item.find_element_by_class_name('countryOfCitizenship').text
        except Exception as ex:
            country = 'NAN'

        try:
            source = item.find_element_by_class_name('source').text
        except Exception as ex:
            source = 'NAN'

        try:
            industry = item.find_element_by_class_name('industries').text
        except Exception as ex:
            industry = 'NAN'
        
        info = {
            "rank" : rank,
            "name" : name,
            "net" : net,
            "age" : age,
            "country" : country,
            "source" : source,
            "industry" : industry
        }

        json.dump(info, f, indent=4)

    f.close()

data = []

def links():
    rank = 0
    for item in allInfo: # parcurg toate clasele ascunse
        rank = rank + 1
        try:
            link = item.find_element_by_class_name('bio-button').get_attribute('href') # obtin link-ul din fiecare clasa
        except Exception as ex:
            link = 'NAN'
        
        data.append([rank, link]) # adaug fiecare link + rank-ul intr-o lista


def stats():
    #for row in data:
        #print(row)
    nr = 0
    for i in range(2):
        nr = nr + 1
        driver.get(data[i][1]) #row[1]  # data[i][1] # accesez fiecare link
        driver.implicitly_wait(10)
        sts = driver.find_element_by_class_name('profile-stats')   # gasesc clasa care ma intereseaza
        text = sts.find_elements_by_class_name('profile-stats__text') # parcurg clasa si clasele subordonate si iau informatiile care ma intereseaza
        title = sts.find_elements_by_class_name('profile-stats__title')
        info = {
        }
        for i in range(len(title)):
            #print(title[i].text + '   ' + text[i].text)
            info["RANK"] = nr
            info[title[i].text] = text[i].text
            
        json.dump(info, g, indent=4)
    g.close()


links()
#print(len(data))
stats2()
