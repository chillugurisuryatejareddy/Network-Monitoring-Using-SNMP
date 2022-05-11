#!/usr/bin/python3
import easysnmp    
from easysnmp import snmp_get
from easysnmp import snmp_walk
from easysnmp import Session
import sys
import time
import math

agent_details = sys.argv[1]
info = agent_details.split(':')
agent_ip = info[0]
agent_port = info[1]
agent_comm = info[2]
frequency = float(sys.argv[2])
samples_count = int(sys.argv[3])
sample_time = 1/frequency
s_oids = []
list_oid1=[]
list_oid2=[]
uclock=""
timer1=0

for i in range(4,len(sys.argv)):
	s_oids.append(sys.argv[i])
	
s_oids.insert(0,'1.3.6.1.2.1.1.3.0')


def getter():
	global list_oid1, timer1, uclock, list_oid2
	
	if output[j].value!='NOSUCHOBJECT' and output[j].value!='NOSUCHINSTANCE':
		list_oid2.append(int(output[j].value))
		if count!=0 and len(list_oid1)>0:
			onida = int((list_oid2[j-1])) - int((list_oid1[j-1]))
			#print(onida)
			diff_time = ((k) - (timer1))
			#print(diff_time)
			rate = int((onida)/(diff_time))
			if rate < 0:
				if output[j].snmp_type == 'COUNTER32':
					onida = onida + (2**32)
					try:
						if uclock==str(timer2):
							print(str((onida/diff_time)),end="|")
							uclock=str(timer2)
						elif uclock=="":
							print(str(timer2) +"|"+ str(round(onida/diff_time)),end="|");uclock=str(timer2)
						else:
							print(str(timer2) +"|"+ str(round(onida/diff_time)),end="|");uclock=str(timer2)

					except:
						print(str(timer2) +"|"+ str(round(onida/diff_time)), end= "|");uclock=str(timer2)

				elif output[j].snmp_type == 'COUNTER64':
					onida=onida+2**64					
					try:
						if uclock==str(timer2):
							print(str(onida/diff_time), end ="|")
							uclock=str(timer2)
						elif uclock=="":
							print(str(timer2) +"|"+ str(round(onida/diff_time)), end="|");uclock=str(timer2)
						else:
							print(str(timer2)+ "|"+ str(round(onida/diff_time)) ,end="|");uclock=str(timer2)
					except:
						print(str(timer2)+ "|"+ str(round(onida/diff_time)),end= "|");uclock=str(timer2)

			else:	
				try:
					if uclock==str(timer2):
						print(str(rate),end= "|")
						uclock=str(timer2)
					elif uclock=="":
						print(str(timer2) +"|"+str(round(rate)),end="|")
						uclock=str(timer2)
					else:
						print(str(timer2) +"|"+str(round(rate)),end="|") 
						uclock=str(timer2)
				except:
					print(str(timer2) +"|"+ str(round(rate)), end = "|")  
					uclock=str(timer2)	

def octetstr():
	global list_oid1, timer1, uclock, list_oid2
	
	if output[j].value!='NOSUCHOBJECT' and output[j].value!='NOSUCHINSTANCE':
		list_oid2.append((output[j].value))
		if count!=0 and len(list_oid1)>0:
			try:
				if uclock==str(timer2):
					print(str(list_oid2[len(list_oid2)-1]),end= "|")
					uclock=str(timer2)
				elif uclock=="":
					print(str(timer2) +"|"+ str(list_oid2[len(list_oid2)-1]),end="|") 
					uclock=str(timer2)		
				else:
					print(str(timer2) +"|"+ str(list_oid2[len(list_oid2)-1]), end="|") 
					uclock=str(timer2)
			except:

				print("\n"+str(timer2) +"|"+ str(list_oid2[len(list_oid2)-1]),end="|")  
				uclock=str(timer2)

def gauge():
	global list_oid1, timer1, uclock, list_oid2
	
	if output[j].value!='NOSUCHOBJECT' and output[j].value!='NOSUCHINSTANCE':
		list_oid2.append(int(output[j].value))
		if count!=0 and len(list_oid1)>0:
			onida = (list_oid2[j-1]) - (list_oid1[j-1])
			if onida>0: onida ="+"+str(onida)
			try:
				if uclock==str(timer2):
					print(str(list_oid2[len(list_oid2)-1])+"("+str(onida)+")" ,end= "|")
					uclock=str(timer2)
				elif uclock=="":
					print(str(timer2) +"|"+ str(list_oid2[len(list_oid2)-1])+"("+str(onida)+")",end="|") 
					uclock=str(timer2)			
				else:
					print(str(timer2) +"|"+ str(list_oid2[len(list_oid2)-1])+"("+str(onida)+")", end="|") 
					uclock=str(timer2)
			except:
				print("\n"+str(timer2) +"|"+ str(list_oid2[len(list_oid2)-1])+"("+str(onida)+")", end = "|")  
				uclock=str(timer2)			

if samples_count==-1:
	session=Session(hostname=agent_ip,remote_port=agent_port,community=agent_comm,version=2,timeout=0.1,retries=10)
	count = 0
	list_oid1 = []
	while True:
		timer2=float(time.time())
		output = session.get(s_oids)
		k=float(output[0].value)/100
		list_oid2 = []
		j=1
		if count>0:
			if k<timer1:
				print("system restarted")
				continue
		while j<len(output):
			m=output[j].snmp_type
			if m =='COUNTER' or m == 'COUNTER64' or m == 'COUNTER32':
				getter()
			elif m =='GAUGE':
				gauge()
			elif m =='OCTETSTR':
				octetstr()
			j=j+1
		list_oid1=list_oid2
		timer1 = k
		if count!=0:
			print(end="\n")
		q=float(time.time())
		count=count+1
		if sample_time<(q-timer2):
			n=math.ceil((q-timer2)/sample_time)
			time.sleep((n*sample_time) - q + timer2)
		else:
			time.sleep(sample_time-q+timer2)	
else:
	session=Session(hostname=agent_ip,remote_port=agent_port, community=agent_comm ,version=2,timeout=0.1,retries=10)
	list_oid1 = []
	for count in range(0,samples_count+1):
		timer2=float(time.time())
		output = session.get(s_oids)
		k=int(output[0].value)/100		
		list_oid2 = []
		j=1
		if count>0:
			if k<timer1:
				print("system restarted")
				break
		while j<len(output):
			m=output[j].snmp_type
			if m =='COUNTER' or m == 'COUNTER64' or m == 'COUNTER32':
				getter()
			elif m =='GAUGE':
				gauge()
			elif m =='OCTETSTR':
				octetstr()
			j=j+1
		list_oid1=list_oid2
		timer1 = k
		if count!=0:
			print(end="\n")
		q=float(time.time())
		f=q - timer2
		if f>sample_time:
			n=math.ceil(f/sample_time)
			time.sleep((n*sample_time) - f)
		else:
			time.sleep(sample_time - f)
