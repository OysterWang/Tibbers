#coding:utf-8
import threading
import time, re
from subprocess import Popen, PIPE

import utils.parse_geo
import utils.parse_ipinfo

point_return = {}

def tmp_trace_txt_url(domain_str):
	tmp_trace_txt_url = "tmp/trace_"	#web用
	#tmp_trace_txt_url = "../tmp/trace_"	#测试用
	return tmp_trace_txt_url + domain_str + ".txt"

class TraceThread(threading.Thread):
	def __init__(self, domain_str):
		threading.Thread.__init__(self)
		self.domain_str = domain_str
		self.cmd_str = "tracert -d " + self.domain_str
		self.ip_list = []
		print("%s created!" %self.getName())
		print("%s domain_str : %s "%(self.getName(), self.domain_str))
		print("%s cmd_str : %s"%(self.getName(), self.cmd_str))
		self.trace_txt = open(tmp_trace_txt_url(self.domain_str),"w")

	def trace_extract_save(self):
		regex_ip = re.compile('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|\*{1,3})')
		p = Popen(self.cmd_str, stdout=PIPE)
		num = 0
		while True:
			one_line = p.stdout.readline()
			if not one_line:
		   		break
			ip_extract = regex_ip.findall(one_line.decode('gbk')) #抽出含有ip的每一hop  one_line.decode('gbk')
			if len(ip_extract) >= 1:	#含有ip或者*的行要保存
				num += 1
				self.trace_txt.write(one_line.decode('gbk').strip("\n"))	#oneline存入txt中	one_line.decode('gbk')
				self.trace_txt.flush()
				#print("%s : write line[%d] ip:%s  %s" %(self.getName(), num, ip_extract[0], one_line))			
		self.trace_txt.close()
		
	def run(self):
		self.trace_extract_save()
		print ("%s-tracert %s end!"%(self.getName(), self.domain_str))
		print ("%s over" %self.getName())

class SeekThread(threading.Thread):
	def __init__(self, domain_str, need_seq):
		threading.Thread.__init__(self)
		self.domain_str = domain_str
		self.need_seq = need_seq
		self.target_ip = ""
		#self.point = []
		self.ip_list = []
		self.readLinesNum = 70
		self.regex_ip = re.compile('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|\*{1,3})')
		print("******%s created. Need lines[%d]" %(self.getName(), self.need_seq))
	
	def seekSeq(self):
		loop_time = 1
		global point_return
		while True:
			time.sleep(1)
			self.trace_txt = open(tmp_trace_txt_url(self.domain_str),"r")
			print("******%s the %d time open txt to seek lines[%d]" %(self.getName(), loop_time, self.need_seq))
			loop_time += 1
			flag = 0
			self.ip_list = []

			try:
				#new
				while True:
					line = self.trace_txt.readline()
					
					print("******%s flag: %d origin line: %s" %(self.getName(), flag, line))
					if not line:
						print("******%s not line check , len(self.ip_list) = %d" %(self.getName(), len(self.ip_list)))
						#检查是否已经trace完，判断上一个seq请求的是否已经是target_ip
						if self.ip_list[len(self.ip_list) - 1] == self.target_ip:
							point = {}
							point['flag'] = 0
							print("******%s already to the last hop" %(self.getName()))
							print("******%s make it into point: %s" %(self.getName(), point))
							point_return = point
							return
						break	#重新open

					if flag == 0:	#此行是第一行
						ip_extract = self.regex_ip.findall(line)
						self.target_ip = ip_extract[0]
						flag += 1
						#print("******%s line[0]: %s" %(self.getName(), line))
						#print("******%s target_ip: %s" %(self.getName(), self.target_ip))
						continue
					else:	#此行不是第一行
						if self.need_seq == flag:	#到了need_seq行
							ip_extract = self.regex_ip.findall(line)
							if len(ip_extract) >= 1:
								point = {}
								#point["flag"] = 1  #常量
								#point["seq"] = self.need_seq	#传参
								#point["ip"] = ip_extract[0]	#传参
								#point["city"] = "Tianjin"	#需parse
								#point["coord"] = [117.20000,39.13333]	#需parse
								#point = utils.parse_geo.parse_geo(ip_extract[0], self.need_seq)	#geo tool
								point = utils.parse_ipinfo.parse_ipinfo(ip_extract[0], self.need_seq)	#ipinfo tool
								self.ip_list.append(ip_extract[0])
								print("******%s find lines[%d]: %s  %s"%(self.getName(), self.need_seq, ip_extract[0], line))
								print("******%s make it into point: %s" %(self.getName(), point))
								print("******%s len(self.ip_list) = %d" %(self.getName(), len(self.ip_list)))
								point_return = point
								return
								#return point
						else:	#未到need_seq行，加入list
							print("******%s not yet line[%d/%d]: %s" %(self.getName(), flag, self.need_seq, line))
							ip_extract = self.regex_ip.findall(line)
							if len(ip_extract) >= 1:
								self.ip_list.append(ip_extract[0])
							flag += 1
							continue
				#new
				'''
				if lines[self.need_seq]:	#需要的seq不为空则说明找到，生成point返回
					ip_extract = self.regex_ip.findall(lines[self.need_seq])
					if len(ip_extract) >= 1:
						print("******%s find lines[%d]: %s"%(self.getName(), self.need_seq, ip_extract[0]))	#.decode('gbk')
						point = {}
						point['flag'] = 1
						point['seq'] = seq
						point['city'] = ""
						point['ip'] = ip_extract[0]
						point['coord'] = []
						self.ip_list.append(ip_extract[0])	#ip存入ip_list
						#self.points.append(point)
						print("%s make into point: %s" %(self.getName(), point))
						mutex.release()
						return point
				'''
			except Exception as ex:
				print("******%s Exception: %s" %(self.getName(), ex))
				continue	#重新open

	def run(self):
		self.seekSeq()
		print ("******%s over" %self.getName())

if __name__ == "__main__":
	global point_return
	traceThread = TraceThread("www.baidu.com")
	traceThread.start()
	time.sleep(1)
	seekThread = SeekThread("www.baidu.com", 3)
	seekThread.start()
	time.sleep(10)
	print("I need%s" %point_return)

	
