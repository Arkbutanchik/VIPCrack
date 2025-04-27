from fabric import Connection

HOST = '192.168.1.9'
USER = 'arkbutan'
PASSWD = 'arkbutan'

def run_ssh_command(command):

    conn = Connection(host=HOST, user=USER, connect_kwargs={'password': PASSWD})

    return conn.run(command, hide=True).stdout.split('\n')


for i in run_ssh_command('ls'):
    print(run_ssh_command(f'cd {i} && ls'))