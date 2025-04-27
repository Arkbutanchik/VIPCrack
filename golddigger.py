from fabric import Connection
import argparse


parser = argparse.ArgumentParser()
    
parser.add_argument('-H', '--host', dest='HOST', required=True, help='Target host IP address')
parser.add_argument('-u', '--user', dest='USER', required=True, help='Username for authentication')
parser.add_argument('-p', '--pass', dest='PASSWD', required=True, help='Password for authentication')
    
args = parser.parse_args()
    
HOST = args.HOST
USER = args.USER
PASSWD = args.PASSWD
    
print(f"Connecting to {HOST} with user {USER} and password {PASSWD}")
    

def run_ssh_command(command):

    conn = Connection(host=HOST, user=USER, connect_kwargs={'password': PASSWD})

    return conn.run(command, hide=True).stdout.split('\n')

for i in run_ssh_command('ls'):
    print(run_ssh_command(f'cd {i} && ls'))
