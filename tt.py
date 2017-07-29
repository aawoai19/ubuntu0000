#!/usr/bin/python
#coding=utf-8

from getjijinline import test as jz

if __name__ == '__main__':
    num = raw_input('基金号：\n')
    jz.getdata(num)
    day1 = int(raw_input('\n1:\n'))
    day2 = int(raw_input('\n2:\n'))
    jz.paint(num,day1,day2)