#coding:utf-8
import threading
import time, re
from subprocess import Popen, PIPE


class TraceThread(threading.Thread):
	def __init__(self, domain_str):
		threading.Thread.__init__(self)
		self.domain_str = domain_str
		self.cmd_str = "tracert -d " + self.domain_str
		self.ip_list = []
		self.points = []
		print("")
		print("TraceThread-domain_str : %s "%(self.domain_str))
		print("TraceThread-cmd_str : %s"%self.cmd_str)
		self.trace_txt = open("tmp/trace_"+domain_str+".txt","w")

	def trace_and_extract(self):
		regex_ip = re.compile('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|\*{1,3})')
		p = Popen(self.cmd_str, stdout=PIPE)
		seq = 0
		target_ip = ""
		while True:
			one_line = p.stdout.readline().decode('gbk')
			if not one_line:
		   		break
			#print("one_line:%s"%one_line)
			ip_extract = regex_ip.findall(one_line) #抽出每一hop中的ip list

			#print("ip_extract:%s"%ip_extract)
			if len(ip_extract) >= 1:
				self.trace_txt.write(one_line)	#oneline存入txt中
				if seq == 0:	#第一个ip为目的ip，非hop中的
					target_ip = ip_extract[0]
					seq += 1
					continue
				else: #第二个ip开始存入points列表中
					point = {}
					point['flag'] = 1
					point['seq'] = seq
					point['city'] = ""
					point['ip'] = ip_extract[0]				
					point['coord'] = []
					self.points.append(point)
					self.ip_list.append(ip_extract[0])
					#print ("points%s"%self.points)
					print("TraceThread-IP: %s %s"%(ip_extract[0], one_line))
					seq += 1
		self.trace_txt.close()

	def run(self):
		self.trace_and_extract()
		point = {}
		point['flag'] = 0
		self.points.append(point)	#trace结束
		print ("TraceThread-points%s"%self.points)
		print ("TraceThread-ip_list:%s"%self.ip_list)
		print ("TraceThread-tracert %s end!"%self.domain_str)

class SeekThread(threading.Thread):
	def __init__(self, seq):
		print("in SeekThread")
		threading.Thread.__init__(self)
		self.trace_txt = open("tmp/trace_"+domain_str+".txt","r")

	def seekSeq(self, seq):
		for line in self.trace_txt:
			print("read: " +line)

	def run(self):
		self.seekSeq(seq)

if __name__ == "__main__":
	traceThread = TraceThread("123.125.248.90")
	traceThread.start()
	time.sleep(1)
	seekThread = SeekThread(1)
	seekThread.start()