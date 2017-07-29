#!/usr/bin/python
#coding=utf-8

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

driver = webdriver.PhantomJS()
waite = WebDriverWait(driver,5)
jingzhi = {}


def isprased(xpath):
    return EC.presence_of_element_located((By.XPATH,xpath))

def quickopen(num):
    jingzhi[num] = {}
    url = 'http://fund.eastmoney.com/f10/jjjz_%s.html'%num
    driver.get(url)
    waite.until(EC.title_contains(num))
    return driver

def save_20d_jingzhi(num,fnum):
    for i in range(1,21):
        date = driver.find_element_by_xpath('//*[@id="jztable"]/table/tbody/tr[%s]/td[1]'%i).text
        path = driver.find_element_by_xpath('//*[@id="jztable"]/table/tbody/tr[%s]/td[3]'%i).text
        path = float(path)
        snum = fnum*20 + i
        jingzhi[num][snum]=[date,path]
    return True

def getdata(num):
    driver = quickopen(num)
    for i in range(0,7):
        waite.until(isprased('//*[@id="jztable"]/table/tbody/tr[20]/td[1]'))
        save_20d_jingzhi(num,i)
        driver.find_element_by_xpath('//*[@id="pagebar"]/div[1]/label[8]').click()
    return jingzhi[num]

def paint(num,day1,day2):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as pl
    data = jingzhi[num]
    x1 =[]
    y1 = []
    x2 = []
    y2 = []
    for i in range(0,100):
        xx1 = 100-i
        it = i+1
        yyy = 0
        for d in range(0,day1):
            it2 = i+d+1
            yyy += data[it2][1]
        yy1 = yyy/day1
        xx2 = xx1
        yyy = 0
        for d in range(0,day2):
            it2 = i+d+1
            yyy += data[it2][1]
        yy2 = yyy/day2
        x1.append(xx1)
        y1.append(yy1)
        x2.append(xx2)
        y2.append(yy2)
    pl.plot(x1, y1, 'r')  # use pylab to plot x and y
    pl.plot(x2, y2, 'g')
    pl.xlim(0, 100)  # set axis limits
    pl.ylim(min(y1), max(y1))
    pl.savefig('/home/ubuntu0000/work/thisfig.pdf')

if __name__ == '__main__':
    try:
        num = raw_input('请输入基金号:\n')
        print '请耐心等待......'
        getdata(num)
        day1 = raw_input('\n请输入平均天数1:\n')
        day1 = int(day1)
        day2 = raw_input('\n请输入平均天数2:\n')
        day2 = int(day2)
        paint(num,day1,day2)
    finally:
        driver.quit()