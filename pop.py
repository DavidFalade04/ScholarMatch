from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.chrome.options import Options
import time
import sqlite3

conn = sqlite3.connect("scholarship.db")
cursor = conn.cursor()

#make it run in the background
chrome_options = Options()

#Open browser and website
driver = webdriver.Chrome(executable_path=r"C:\Users\David\Coding\chromedriver.exe",chrome_options=chrome_options)
driver.get("https://www.scholarshipscanada.com")

def populate():
    page = driver.find_element(By.ID, "Page-Content-All")
    div = page.find_element(By.ID, "ctl00_ContentPlaceHolder1_RightUserControl_pnlScholarshipFilter")
    count = cursor.execute("SELECT * FROM FOS LIMIT 1")
    rows = count.fetchall()
    if not rows:
        fos = div.find_element(By.ID, "ctl00_ContentPlaceHolder1_RightUserControl_ddlFieldofStudy")
        fields = fos.find_elements(By.TAG_NAME, "option")
        for field in fields:
            cursor.execute("INSERT INTO FOS(name) VALUES(?)",(field.text,))
     
    count = cursor.execute("SELECT * FROM schools LIMIT 1")
    rows = count.fetchall()
    if not rows:
        sl = div.find_element(By.ID,"ctl00_ContentPlaceHolder1_RightUserControl_ddlSchool")
        schools = sl.find_elements(By.TAG_NAME, "option")
        for school in schools:
            cursor.execute("INSERT INTO schools(name) VALUES (?)", (school.text,)) 

    count = cursor.execute("SELECT * FROM ROS LIMIT 1")
    rows = count.fetchall()
    if not rows:
        ros = div.find_element(By.ID,"ctl00_ContentPlaceHolder1_RightUserControl_ddlRegionofStudy")
        regions = ros.find_elements(By.TAG_NAME, "option")
        for region in regions:
            cursor.execute("INSERT INTO ros(name) VALUEs (?)",(region.text,))

    count = cursor.execute("SELECT * FROM heritage LIMIT 1")
    rows = count.fetchall()   
    if not rows:
        htg = div.find_element(By.ID,"ctl00_ContentPlaceHolder1_RightUserControl_chkHeritage")
        heritages = htg.find_elements(By.TAG_NAME, "label")
        for heritage in heritages:
            cursor.execute("INSERT INTO heritage(name) VALUES (?)", (heritage.text,))
        
    count = cursor.execute("SELECT * FROM pc LIMIT 1")
    rows = count.fetchall()   
    if not rows:
        pc = div.find_element(By.ID,"ctl00_ContentPlaceHolder1_RightUserControl_chkPersonal")
        circumstances = pc.find_elements(By.TAG_NAME, "label")
        cursor.execute("INSERT INTO pc(name) VALUES('Any')")
        for circumstance in circumstances:
            cursor.execute("INSERT INTO pc(name) VALUES (?)", (circumstance.text,))

    

def search():
    search = driver.find_element_by_id("txtScholarshipSearch")
    search.send_keys("black")
    search.send_keys(Keys.RETURN)

        
   
search()

populate()

conn.commit()
conn.close()

time.sleep(5)
driver.quit()
