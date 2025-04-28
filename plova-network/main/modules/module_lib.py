import os

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

def module_lib():
	print("\nAvailable modules:")
	print("------------------------")
	print(f"{Fore.BLUE}net/arp_poison")
	print(f"net/tcp_reset")
	print(f"bluetooth/ble_dos{Style.RESET_ALL}\n")
	return
