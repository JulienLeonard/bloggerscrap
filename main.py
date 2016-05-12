from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import selenium
import sys
import time
import urllib



def getpostdata(driver,url):

    driver.get(url)

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "post-body"))
        )
    finally:
        print "error"


    elems = driver.find_elements(By.CLASS_NAME, 'post-title')
    title = elems[0].text.strip()

    elems = driver.find_elements(By.CLASS_NAME, 'date-header')
    timestamp = elems[0].text.strip()

    elems = driver.find_elements(By.CLASS_NAME, 'blog-pager-older-link')
    nextlink = None
    if len(elems) > 0:
        nextlink = elems[0].get_attribute("href")

    # save image
    elems = driver.find_elements(By.XPATH, '//img')
    imagelink = elems[0].get_attribute("src")
    imagename = imagelink.split('/')[-1]
    urllib.urlretrieve(imagelink, "images/"+imagename)
        
    result = {"title":title, "timestamp":timestamp, "link":nextlink, "image":imagename}
        
    return result


    

#
# fetch faa stats and dump them into xml file
#
def main():

    # create selenium webdriver
    driver = webdriver.Firefox()

    cpost = "http://fractalyze.blogspot.sg/2016/05/helicoidal.html"
    content = ["* fractalyze"]

    nmaxposts = 10000000000
    nposts = 0
    while len(cpost) > 0:
        postdata = getpostdata(driver,cpost)
        content.append("** " + str(postdata["title"]))
        content.append("blogger_link : "  + str(cpost))
        content.append("blogger_timestamp : "  + str(postdata["timestamp"]))
        content.append("blogger_image : file://c:/DEV/bloggerscrap/images/" + str(postdata["image"]))

        print("new post" + " -- ".join(content))
        
        cpost = postdata["link"]
        time.sleep(1)

        nposts +=1
        if nposts > nmaxposts:
            break
        

    # dump org into outputfile
    output=open("blogger.org", 'w+')
    output.write("\n".join(content).encode('utf8'))
    output.close()
    
main()

