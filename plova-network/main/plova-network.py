import os
import subprocess
import readline

from time import sleep
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

from modules import tcp_reset
from modules import arp_poison
from modules import module_lib
from modules import bluetooth_dos

def banner():
	version="0.0.1"
	print('    ____  __ _    __      _   _______________       ______  ____  __ __')
	sleep(0.15)
	print('   / __ \\/ /| |  / /     / | / / ____/_  __/ |     / / __ \\/ __ \\/ //_/')
	sleep(0.15)
	print('  / /_/ / / | | / /_____/  |/ / __/   / /  | | /| / / / / / /_/ / ,<   ')
	sleep(0.15)
	print(' / ____/ /__| |/ /_____/ /|  / /___  / /   | |/ |/ / /_/ / _, _/ /| |  ')
	sleep(0.15)
	print('/_/   /_____/___/     /_/ |_/_____/ /_/    |__/|__/\\____/_/ |_/_/ |_|  \n\n')
	sleep(0.25)
	print(f"{Fore.BLUE}by plova" + "                                            " + f"version {Style.RESET_ALL}" + version + '\n')
	return
	


def cinput():
	inp0 = f"{Fore.GREEN}plv>{Style.RESET_ALL}"
	cmd=input(inp0).lower()
	if(cmd[0:5]=="help"):
		print("\nCommands:\n------------------------------\nshow modules - List available modules\nuse [module] - Use the selected module\nhelp - Displays this message\nexit - Quit the application\n")
	elif(cmd[0:13]=="show modules"):
		module_lib.module_lib()
	elif(cmd[0:5]=="exit"):
		print("\nGood luck, Plova!")
		exit(0)
	elif(cmd[0:3]=="use"):
		if(cmd[4:18] == "net/arp_poison"):
			print("\nUsing ARP poisoning MiTM attack!\n")
			arp_poison.arp_spoof()
		elif(cmd[4:17] == "net/tcp_reset"):
			print("\nUsing TCP [RST] flag attack!\n")
			tcp_reset.tcp_reset()
		elif(cmd[4:21] == "bluetooth/ble_dos"):
			print("\nUsing Bluetooth DoS attack!\n")
			bluetooth_dos.bluetooth_dos()
		else:
			print('\nUnknown module!\n')
	else:
		print("\nUnknown command! Use 'help' for info\n")
			
	cinput()	

banner()
cinput()
