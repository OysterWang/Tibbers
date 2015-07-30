#coding: utf-8
import threading
import time

global num
num = 0
def test():
	global num
	num = 2
	print num

def test2():
	print num
if __name__ == '__main__':
	test()
	test2()
