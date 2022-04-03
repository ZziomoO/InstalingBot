from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import datetime
import time
import json

browser = webdriver.Firefox()

def UsersSetup():
    usersFile = open('user.json')
    usersData = json.load(usersFile)
    usersFile.close()
    Date = datetime.datetime.now().strftime("%x")
    for x in usersData:
        if x['last'] == Date:
            continue
        LoginForm(x['login'],x['password'])
        x['last'] = Date
        usersFile = open('user.json', "w")
        json.dump(usersData, usersFile)
        usersFile.close()
    browser.quit()

def LoginForm(login,password):
    browser.get("https://instaling.pl/teacher.php?page=login")
    DoAction(1,True,'//*[@id="log_email"]',1,login)
    DoAction(1,True,'//*[@id="log_password"]',1,password)
    DoAction(2,True,'/html/body/div/div[3]/form/div/div[3]/button')
    DoAction(2,True,'//*[@id="student_panel"]/p[1]/a')
    time.sleep(0.5)
    DoAction(2,False,'#continue_session_button')
    DoAction(2,False,'#start_session_button')
    UsersLoop()

def UsersLoop():
    while True:
        if IsSessionEnded():
            DoAction(2,True,'//*[@id="student_panel"]/p[9]/a')
            break
        DoAction(2,False,'#know_new')
        DoAction(2,False,'#skip')
        DoAction(2,True,'//*[@id="nextword"]')
        if not IsAnswerPage():
            continue
        addToArray = True
        polishWord = DoAction(3,True,'//*[@id="question"]/div[2]/div[2]')
        polishSentence = DoAction(3,True,'//*[@id="question"]/div[1]')
        wordsFile = open('word.json')
        wordsData = json.load(wordsFile)
        wordsFile.close()
        for x in wordsData:
            if polishWord == x['word'] and polishSentence == x['sentence']:
                addToArray = False
                englishWord = x['translation']
                break
        if not addToArray:
            DoAction(1,True,'//*[@id="answer"]',1,englishWord)
        time.sleep(0.5)
        DoAction(2,True,'//*[@id="check"]')
        englishWord = DoAction(3,True,'//*[@id="word"]')
        if addToArray:
            newJSON = {'word': polishWord, 'sentence': polishSentence, 'translation': englishWord}
            wordsData.append(newJSON)
        if not addToArray:
            for x in wordsData:
                if polishWord == x['word'] and polishSentence == x['sentence']:
                    x['translation'] = englishWord
                    break
        usersFile = open('word.json', "w")
        json.dump(wordsData, usersFile)
        usersFile.close()
        time.sleep(0.5)

def DoAction(action,type,path,time = 1,keys = None):
    element = CreateWait(type,path,time)
    try:
        if action == 1:
            element.send_keys(keys)
        elif action == 2:
            element.click()
        elif action == 3:
            return element.get_attribute('innerHTML')
    except:
        pass

def CreateWait(type,path,time):
    if type:
        type = By.XPATH
    else:
        type = By.CSS_SELECTOR
    try:
        return WebDriverWait(browser, timeout=time).until(lambda d: d.find_element(type,path))
    except:
        pass

def IsSessionEnded():
    try:
        browser.find_element(By.CSS_SELECTOR,'#return_mainpage').click()
    except:
        return False
    else:
        return True

def IsAnswerPage():
    try:
        browser.find_element(By.XPATH, '//*[@id="answer"]')
    except:
        return False
    else:
        return True

UsersSetup()     
