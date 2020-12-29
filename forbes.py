from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd="root", database="py_project")
mycursor = mydb.cursor()
'''
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
'''
def completeList():
    nr = 0
    for item in all:
        nr = nr + 1
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
            "id" : nr,
            "rank" : rank,
            "name" : name,
            "net" : net,
            "age" : age,
            "country" : country,
            "source" : source,
            "industry" : industry
        }

        json.dump(info, f, indent=4)

        sql = "INSERT INTO completelist (`id`,`rank`,`name`,`netWorth`,`age`,`country`,`source`,`industry`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"  
        val = (nr, rank, name, net, age, country, source, industry)
        mycursor.execute(sql, val)

        mydb.commit()

    f.close()

data = []

def links():
    id = 0
    for item in allInfo: # parcurg toate clasele ascunse
        id = id + 1
        try:
            link = item.find_element_by_class_name('bio-button').get_attribute('href') # obtin link-ul din fiecare clasa
        except Exception as ex:
            link = 'NAN'
        
        data.append([id, link]) # adaug fiecare link + id-ul intr-o lista


def stats():
    nr = 0
    for row in data:
        #print(row)
     #for i in range(2):
        nr = nr + 1
        driver.get(row[1]) #row[1]  # data[i][1] # accesez fiecare link
        driver.implicitly_wait(10)
        sts = driver.find_element_by_class_name('profile-stats')   # gasesc clasa care ma intereseaza
        text = sts.find_elements_by_class_name('profile-stats__text') # parcurg clasa si clasele subordonate si iau informatiile care ma intereseaza
        title = sts.find_elements_by_class_name('profile-stats__title')
        info = {
        }
        info["ID"] = nr

        sql = "INSERT INTO stats (`id`) VALUES (%s)"
        val = (nr,)
        mycursor.execute(sql, val)
        mydb.commit()

        for i in range(len(title)):
            info[title[i].text] = text[i].text
            s = title[i].text.replace(" ", "").replace("-", "").lower()
            if(s == "age" or s == "sourceofwealth" or s == "selfmadescore" or s == "philanthropyscore" or s == "residence" or s == "citizenship" or s == "maritalstatus" or s == "children"): # or s == "education"
                sql = 'UPDATE `stats` SET ' + s + ' = ' + '"' + text[i].text + '"' + ' WHERE `id` = ' + str(nr)
                mycursor.execute(sql)
                mydb.commit()
    
        json.dump(info, g, indent=4)

    g.close()

# o functie care sterge tot din tabele
# o functie care creaza baza de date si tabelele (sa fie acolo desi nu o voi apela la fiecare rulare.. sau poate da, poate trebuie?)
        
#completeList()
#links()
#stats()

def top_10_persoane_tinere():
    sql = "SELECT completelist.id, completelist.rank, completelist.name, stats.age FROM completelist INNER JOIN stats ON completelist.id = stats.id WHERE stats.age IS NOT NULL ORDER BY CAST(stats.age as unsigned) ASC LIMIT 10"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)


def cetatenie_americana():
    sql = "SELECT COUNT(*) FROM stats WHERE citizenship = 'United States' "
    mycursor.execute(sql)
    x = mycursor.fetchone()
    print(x)

def scor_filantropic():
    sql = "SELECT completelist.id, completelist.rank, completelist.name, stats.philanthropyscore FROM completelist INNER JOIN stats ON completelist.id = stats.id WHERE stats.philanthropyscore IS NOT NULL ORDER BY CAST(stats.philanthropyscore as unsigned) DESC LIMIT 10"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)

#top_10_persoane_tinere()
#cetatenie_americana()
scor_filantropic()