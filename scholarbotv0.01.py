from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
import time
import sqlite3
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

conn = sqlite3.connect("scholarship.db")
cursor = conn.cursor()

#Open browser and website
driver = webdriver.Chrome(executable_path=r"C:\Users\David\Coding\chromedriver.exe")
driver.get("https://www.scholarshipscanada.com")

def login():

    #close cookie box
    cookie = driver.find_element(By.ID,"cookieconsent:desc")
    close = driver.find_element(By.CLASS_NAME, "cc-compliance")
    close.click()
    #Search for items
    login = driver.find_element(By.ID, "LoginControl_lblAccessLoginSignin")
    driver.execute_script("arguments[0].click();", login)
    div = driver.find_element(By.ID,"FooterControl_pnlSignIn")
    username = div.find_element(By.ID,"FooterControl_txtUsername")
    password = div.find_element(By.ID, "FooterControl_txtPassword")
    username.send_keys("davidfalade04")
    password.send_keys("Dfalade1186338")
     

    div.find_element_by_id("FooterControl_btnLogin").click()
    search = driver.find_element_by_id("ctl00_ContentPlaceHolder1_RightUserControl_txtScholarshipSearch")
    search.send_keys("foobar")
    search.send_keys(Keys.RETURN)

def search():

    searchtype = driver.find_element_by_id("ctl00_ContentPlaceHolder1_RightUserControl_rblScholarshipSearchBy_0")
    driver.execute_script("arguments[0].click();", searchtype)
    search = driver.find_element_by_id("ctl00_ContentPlaceHolder1_RightUserControl_txtScholarshipSearch")
    search.clear()
    search.send_keys("bc")
    search.send_keys(Keys.RETURN)
    gather()

def gather():

    #load the page
    elements = driver.find_element(By.ID, "Page-Content-All")
   
    #toggle no expired awards
    right = elements.find_element(By.CLASS_NAME,"Content-2Columns")
    block = right.find_element(By.CLASS_NAME, "Right-Navigation-Block")
    filt = block.find_element(By.ID,"ctl00_ContentPlaceHolder1_RightUserControl_pnlScholarshipFilter")
    toggle = filt.find_element(By.ID,"ctl00_ContentPlaceHolder1_RightUserControl_rdbExpiredScholarship")
    no = toggle.find_element(By.ID, "ctl00_ContentPlaceHolder1_RightUserControl_rdbExpiredScholarship_1")
    driver.execute_script("arguments[0].click();", no)
    time.sleep(1)

    #load the page again
    elements = driver.find_element(By.ID, "Page-Content-All")
    div = elements.find_element(By.ID, "ctl00_ContentPlaceHolder1_ScholarshipDataControl_pnlScholarshipList")
    div_child = div.find_element(By.TAG_NAME, "div")
    table = div_child.find_element(By.TAG_NAME, "table")
    tbody = table.find_element(By.TAG_NAME, "tbody")
    column = tbody.find_element(By.CLASS_NAME, "Paging-Standard")
    t1 = column.find_element(By.TAG_NAME,"tr")
    pages = t1.find_elements(By.TAG_NAME,"td")


    flag = True
    while flag:
        result = nav(pages) 
        if result == "empty":
            flag = False
        else:
            pages = result
        conn.commit()

def scrape():
    elements = driver.find_element(By.ID, "Page-Content-All")
    div = elements.find_element(By.ID, "ctl00_ContentPlaceHolder1_ScholarshipDataControl_pnlScholarshipList")
    div_child = div.find_element(By.TAG_NAME, "div")
    table = div_child.find_element(By.TAG_NAME, "table")
    tbody = table.find_element(By.TAG_NAME, "tbody")
    column = tbody.find_element(By.CLASS_NAME, "Paging-Standard")

    #iterate through pages
    for item in range(2):
        #gets the page content
        elements = driver.find_element(By.ID, "Page-Content-All")
    
        #gets the div that holds the table
        div = elements.find_element(By.ID, "ctl00_ContentPlaceHolder1_ScholarshipDataControl_pnlScholarshipList")
        #gets the table
        div_child = div.find_element(By.TAG_NAME, "div")
        table = div_child.find_element(By.TAG_NAME, "table")
        tbody = table.find_element(By.TAG_NAME, "tbody")
        rows = tbody.find_elements(By.TAG_NAME, "tr")

        #accesses individual rows
        for row in rows:
            #get row contents
            contents = row.find_elements(By.TAG_NAME, "a")
            #get scholarship name and school
            if len(contents) > 1:
                ssName = contents[0]
                ssSchool = contents[1].text
                href = contents[0].get_attribute('href')
                if contents[1].text == "more...":
                    ssSchool = "Any"
            elif len(contents) == 1:
                ssName = contents[0]
                ssSchool = "Any"
            #get the table data
            td = row.find_elements(By.TAG_NAME, "td")
            #get the field of study by scanning the text for the word field of study
        
            #makes sure it only works on rows that have table data one    
            cash = None
            date = None
            if len(td) > 1:
                text = td[1].text.split("Study: ")
                #format field of study so it matches database
                if len(text) > 1:
                    text = text[1].replace("; ", ";")
                    fields = text.split(";")
        
            
                #get cash amount and date
                cash = td[2].text
                date = td[3].text

                #demonstrate
                print( ssName.text + " " + cash + " " + date)
                #Insert Scholarships in scholarships table
                x = cursor.execute("INSERT OR IGNORE INTO scholarships(name, amount, DUE_DATE, link) VALUES(?,?,?,?) RETURNING *",(ssName.text,cash, date,href))
            
                if list(x):

                #Insert Relation between field of study and scholarships
                    for field in fields:
                        cursor.execute("INSERT OR IGNORE INTO SS_FOS(ssid,FOSid) VALUES((SELECT id FROM scholarships WHERE name = ?),(SELECT id FROM FOS WHERE name =?))",(ssName.text,field))

            #Insert Relationship between school and Scholarship
                    cursor.execute("INSERT OR IGNORE INTO SS_School(ssid,schoolid) VALUES((SELECT id FROM scholarships WHERE name = ?),(SELECT id FROM schools WHERE name = ?))",(ssName.text,ssSchool))
        
def nav(pages):
    if pages[len(pages)-1].text == ">>": 
        for index in range(len(pages)):
            if pages[index].text == "..." and index > len(pages) / 2:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(pages[index])).click()

                elements = driver.find_element(By.ID, "Page-Content-All")
                div = elements.find_element(By.ID, "ctl00_ContentPlaceHolder1_ScholarshipDataControl_pnlScholarshipList")
                div_child = div.find_element(By.TAG_NAME, "div")
                table = div_child.find_element(By.TAG_NAME, "table")
                tbody = table.find_element(By.TAG_NAME, "tbody")
                column = tbody.find_element(By.CLASS_NAME, "Paging-Standard")
                t1 = column.find_element(By.TAG_NAME,"tr")
                pages = t1.find_elements(By.TAG_NAME,"td")
                scrape()
                print("page:")
                for page in pages:
                    print(page.text)
                return pages

            elif pages[index].text != "<<" and pages[index].text != "...":
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(pages[index])).click()

                elements = driver.find_element(By.ID, "Page-Content-All")
                div = elements.find_element(By.ID, "ctl00_ContentPlaceHolder1_ScholarshipDataControl_pnlScholarshipList")
                div_child = div.find_element(By.TAG_NAME, "div")
                table = div_child.find_element(By.TAG_NAME, "table")
                tbody = table.find_element(By.TAG_NAME, "tbody")
                column = tbody.find_element(By.CLASS_NAME, "Paging-Standard")
                t1 = column.find_element(By.TAG_NAME,"tr")
                pages = t1.find_elements(By.TAG_NAME,"td")
                scrape()

        else:
            for index in reversed(range(len(pages))):
                print(index)
        
        return "empty"


login()
search()

conn.commit()
cursor.close()
time.sleep(5)

driver.quit()
