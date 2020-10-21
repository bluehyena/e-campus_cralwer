import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver

import env

class Todo:
    def __init__(self, todo, classname, point_deadline):
        self.todo_name = todo
        self.class_name = classname
        self.point_deadline = point_deadline

    def __str__(self):
        return "할일 : {} \n과목명 : {}\n점수 및 마감일 : {}".format(self.todo_name, self.class_name, self.point_deadline)

class Notice:
    def __init__(self):
        self.__student_id = env.student_id
        self.__password = env.password
        self.headers = {"User-Agent":env.User_Agent}
        self.browser = webdriver.Chrome()

    def create_soup(self):
        self.soup = BeautifulSoup(self.browser.page_source, "lxml")

    def login(self, url):
        self.browser.get(url)
        self.id_box = self.browser.find_element_by_id("login_user_id")
        self.password_box = self.browser.find_element_by_id("login_user_password")
        self.id_box.send_keys(self.__student_id)
        self.password_box.send_keys(self.__password)
        self.browser.find_element_by_xpath("//*[@id='form1']/div[4]/a").click()
        time.sleep(1)

    def move_to_dashboard(self):
        self.browser.find_element_by_xpath("//*[@id='xn-main']/div/a[2]").click()
        time.sleep(1)
        self.browser.find_element_by_xpath("//*[@id='visual']/div/div[2]/div[2]/div[1]/a").click()
        time.sleep(1)

    def get_todo_list2(self):
        self.create_soup()
        self.tables = self.soup.find_all("li",attrs={"class":"_6q8Mxga _1dyDTaI _1jLfonx _9PzDC58"})
        
        for self.assignment ,self.table in enumerate(self.tables):   
            self.todo = self.table.find("span", attrs={"class":"_3jLMUSh _2QIthAo YQshPr7 _2WOMSfA"}).get_text()
            self.classname = self.table.find("span", attrs={"class":"_3jLMUSh _2QIthAo _1OPt-vm YQshPr7 _2WOMSfA _1bDCVu4"}).get_text()
            self.point_deadline = self.table.find("ul", attrs={"class":"_6q8Mxga _2j92CzO _33c2dII _1eZWDls"}).get_text(" / ")   
            self.assignment = Todo(self.todo, self.classname, self.point_deadline)
            print(self.assignment)
            print("-" * 80)

    def run(self, url):
        self.login(url)
        self.move_to_dashboard()
        self.get_todo_list2()

if __name__ == "__main__":
    url = "https://e-campus.khu.ac.kr/xn-sso/login.php?auto_login=&sso_only=&cvs_lgn=&return_url=https%3A%2F%2Fe-campus.khu.ac.kr%2Fxn-sso%2Fgw-cb.php%3Ffrom%3D%26login_type%3Dstandalone%26return_url%3Dhttps%253A%252F%252Fe-campus.khu.ac.kr%252Flogin%252Fcallback"
    e_campus = Notice()
    e_campus.run(url)