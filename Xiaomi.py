# -*- coding:utf-8 -*-
# coding=utf-8
from selenium import webdriver
import re
import time
import os
import xlwt
from selenium.webdriver.common.keys import Keys
import json
import requests

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time


# sheet1.write(0,2,"追加评论时间")
# sheet1.write(0,3,"追加评论")

options = webdriver.ChromeOptions()
prefs = {
    'profile.default_content_setting_values': {
        'images': 2
    }
}
options.add_experimental_option('prefs', prefs)
class XiaomiComment():
    def __init__(self):
        self.url = 'http://list.mi.com/'
        self.row = 1
        self.col = 0
        self.driver = webdriver.Chrome()
        self.workbook = xlwt.Workbook(encoding='utf-8')
        self.sheet = list

    def get_proxy(self):
        PROXY_POOL_URL = 'http://localhost:5000/get'

        PROXY = 'http://localhost:5000/get'
        try:

            response = requests.get(PROXY_POOL_URL)
            if response.status_code == 200:
                print(response.text)
                return response.text
        except ConnectionError:
            return None

# driver.get(url)
# driver.maximize_window()
    def anti_anti_spider(self):

        self.driver.delete_all_cookies()
        js1= '''Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) '''
        js2= '''window.navigator.chrome = { runtime: {},  }; '''
        js3= '''Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); '''
        js4= '''Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); '''
        self.driver.execute_script(js1)
        self.driver.execute_script(js2)
        self.driver.execute_script(js3)
        self.driver.execute_script(js4)


    def getList(self):
        self.driver.get(self.url)
        self.driver.maximize_window()
        phones = self.driver.find_elements_by_css_selector("a[class='category-list-title']")
        i = 0
        for phone in phones:
            if "小米" in phone.text:
                now_handle = self.driver.current_window_handle
                phone.click()
                self.driver.find_element_by_css_selector("#J_headNav > div > div > div.right > a:nth-child(7)").click()
                self.next_page()
                global sheet
                sheet = list
                sheet[i] = self.workbook.add_sheet(phone.text)  # 新建sheet
                sheet[i].write(0, 0, "评论")
                sheet[i].write(0, 1, "时间")
                self.get_detail()


                i+=1
        return phones


# driver.switch_to.window(driver.window_handles[0])
    def get_detail(self,phones):
        i = 0
        comments = self.driver.find_elements_by_css_selector('div[class="comment-txt"]')
        for comment in comments:
            comment_text = comment.text
            print(comment_text)
            sheet[i].write(self.row, self.col, comment_text)
            self.row += 1
        dates = self.driver.find_elements_by_css_selector('p[class="time"]')
        self.col+=1
        self.row = 1
        for date in dates:
            date_text = date.text
            print(date_text)
            sheet[i].write(self.row,self.col,date_text)
            self.row += 1
        self.row = 1
        self.col = 0

    def next_page(self):
        learn_more = self.driver.find_elements_by_css_selector(
            'body > div.m-comment-wrap.h-comment-wrap > div.container.J_commentWrap > div.row > div.span13.h-comment-main.m-comment-main.J_commentCon > div.m-comment-box.J_commentList > div > a')
        while(len(learn_more)!=0):
            for x in learn_more:
                x.click()

    def run(self):

        self.anti_anti_spider()
        self.get_proxy()
        self.getList()
        self.workbook.save(r'D:\University_study\junior_second half\信息管理课程设计\data\小米6淘宝.xlsx')

if __name__ == '__main__':
    comment = XiaomiComment()
    comment.run()











