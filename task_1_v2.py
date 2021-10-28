from selenium import webdriver
from os.path import abspath
from os import getcwd
import time
from selenium.webdriver import Chrome

class ArticlePage():
    def __init__(self,DRIVERPATH,STARTLINK):
        self.driver = Chrome(DRIVERPATH)
        self.driver.get(STARTLINK)

    def find_all_links(self):
        all_links = self.driver.find_elements_by_xpath("//a[@href]")
        return all_links

    def find_keyword (self):
        keyword_match = False
        if self.driver.find_elements_by_xpath("//*[contains(text(),'Philosophy')]") or \
           self.driver.find_elements_by_xpath("//*[contains(text(),'philosophy')]"):

           keyword_match = True

        return keyword_match

    def click_first_link(self,links_elements):

        for myelement in links_elements:
            element_class = myelement.get_attribute("class")
            element_text = myelement.get_attribute("href")
            # accepts only links,not images or anchors to the same page
            if element_text.find("#") < 0 and element_class != "image" and myelement.text != "edit":
                myelement.click()
                time.sleep(1)
                break

#--------------------------------------------------------------------------------------------------------

DRIVERPATH = abspath(getcwd()) + "/chromedriver.exe."
MAXREDIRECTS = 30
redirections_counter = 0
run_search_keyword = True
STARTLINK = "https://en.wikipedia.org/wiki/Special:Random/article"

TheArticlePage =  ArticlePage(DRIVERPATH,STARTLINK)

while run_search_keyword:
    all_elements = TheArticlePage.find_all_links()
    TheArticlePage.click_first_link(all_elements)
    test = TheArticlePage.find_keyword()

    if redirections_counter == MAXREDIRECTS or test == True:
        run_search_keyword = False
    else:
        redirections_counter = redirections_counter + 1

print ("Task done, number of redirections:",redirections_counter)
