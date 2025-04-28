from fabric import Connection
import argparse
import os

COLORS = {
    'reset': '\033[0m',
    'directory': '\033[33m',
    'image': '\033[32m',
    'text': '\033[31m',
    'other': '\033[34m'
}

ASCII_ART = r'''
                     /$$       /$$       /$$ /$$                                        
                    | $$      | $$      | $$|__/                                        
  /$$$$$$   /$$$$$$ | $$  /$$$$$$$  /$$$$$$$ /$$  /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$ 
 /$$__  $$ /$$__  $$| $$ /$$__  $$ /$$__  $$| $$ /$$__  $$ /$$__  $$ /$$__  $$ /$$__  $$
| $$  \ $$| $$  \ $$| $$| $$  | $$| $$  | $$| $$| $$  \ $$| $$  \ $$| $$$$$$$$| $$  \__/
| $$  | $$| $$  | $$| $$| $$  | $$| $$  | $$| $$| $$  | $$| $$  | $$| $$_____/| $$      
|  $$$$$$$|  $$$$$$/| $$|  $$$$$$$|  $$$$$$$| $$|  $$$$$$$|  $$$$$$$|  $$$$$$$| $$      
 \____  $$ \______/ |__/ \_______/ \_______/|__/ \____  $$ \____  $$ \_______/|__/      
 /$$  \ $$                                       /$$  \ $$ /$$  \ $$                    
|  $$$$$$/                                      |  $$$$$$/|  $$$$$$/                    
 \______/                                        \______/  \______/                     
'''

def parse_arguments():
    parser = argparse.ArgumentParser(description='SSH Filesystem Crawler with Filtering')
    parser.add_argument('-H', '--host', dest='HOST', required=True, help='Target host IP address')
    parser.add_argument('-u', '--user', dest='USER', required=True, help='Username for authentication')
    parser.add_argument('-p', '--pass', dest='PASSWD', required=True, help='Password for authentication')
    parser.add_argument('-d', '--depth', dest='DEPTH', type=int, default=3, help='Maximum recursion depth')
    parser.add_argument('-r', '--root', dest='ROOT', default='/', help='Root directory to start from')
    
    parser.add_argument('-sd', '--show-dirs', dest='SHOW_DIRS', action='store_true', help='Show directories')
    parser.add_argument('-si', '--show-images', dest='SHOW_IMAGES', action='store_true', help='Show image files')
    parser.add_argument('-st', '--show-text', dest='SHOW_TEXT', action='store_true', help='Show text files')
    parser.add_argument('-so', '--show-other', dest='SHOW_OTHER', action='store_true', help='Show other files')
    
    return parser.parse_args()

def run_ssh_command(conn, command):
    try:
        result = conn.run(command, hide=True, warn=True)
        if result.failed:
            return []
        return [line for line in result.stdout.split('\n') if line]
    except Exception as e:
        print(f"Command failed: {command} - {str(e)}")
        return []

def list_directory(conn, path):
    return run_ssh_command(conn, f'ls -A1p "{path}"')

def get_file_type(entry):
    if entry.endswith('/'):
        return 'directory'
    
    _, ext = os.path.splitext(entry)
    ext = ext.lower()
    
    image_exts = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
    if ext in image_exts:
        return 'image'
    
    text_exts = ['.txt', '.log', '.csv', '.json', '.xml', '.yml', '.yaml', '.conf', '.md']
    if ext in text_exts:
        return 'text'
    
    return 'other'

def crawl_filesystem(conn, current_path, args, depth=0):
    if depth > args.DEPTH:
        return []

    try:
        entries = list_directory(conn, current_path)
        if not entries:
            return []

        output = []
        
        for entry in entries:
            clean_entry = entry.rstrip('/')
            full_path = os.path.join(current_path, clean_entry)
            file_type = get_file_type(entry)
            
            show = False
            if file_type == 'directory' and args.SHOW_DIRS:
                show = True
            elif file_type == 'image' and args.SHOW_IMAGES:
                show = True
            elif file_type == 'text' and args.SHOW_TEXT:
                show = True
            elif file_type == 'other' and args.SHOW_OTHER:
                show = True
                
            if not show:
                continue
                
            if file_type == 'directory':
                output.append(f"{COLORS[file_type]}[DIR] {full_path}{COLORS['reset']}")
                output.extend(crawl_filesystem(conn, full_path, args, depth+1))
            else:
                output.append(f"{COLORS[file_type]}[{file_type.upper()}] {full_path}{COLORS['reset']}")
        
        return output
    except Exception as e:
        print(f"Error crawling {current_path}: {str(e)}")
        return []

def main():
    args = parse_arguments()
    
    if not any([args.SHOW_DIRS, args.SHOW_IMAGES, args.SHOW_TEXT, args.SHOW_OTHER]):
        print("Error: No filters specified. Use at least one of -sd, -si, -st, or -so")
        return
    
    print(f'\033[33m{ASCII_ART}\033[0m')
    print(f"Connecting to {args.HOST} with user {args.USER}")
    print(f"Scanning filesystem starting from {args.ROOT} (max depth: {args.DEPTH})")
    
    active_filters = []
    if args.SHOW_DIRS: active_filters.append("directories")
    if args.SHOW_IMAGES: active_filters.append("images")
    if args.SHOW_TEXT: active_filters.append("text files")
    if args.SHOW_OTHER: active_filters.append("other files")
    print(f"Showing: {', '.join(active_filters)}")
    
    try:
        with Connection(
            host=args.HOST,
            user=args.USER,
            connect_kwargs={'password': args.PASSWD},
            connect_timeout=10
        ) as conn:
            hostname = run_ssh_command(conn, 'hostname')
            if not hostname:
                print("Connection test failed")
                return
            print(f"Connected to: {hostname[0]}")
            
            dir_check = run_ssh_command(conn, f'test -d "{args.ROOT}" && echo "exists"')
            if not dir_check or dir_check[0] != "exists":
                print(f"Root directory {args.ROOT} doesn't exist or isn't accessible")
                return
            
            results = crawl_filesystem(conn, args.ROOT, args)
            
            print("\nColor Legend:")
            if args.SHOW_DIRS:
                print(f"{COLORS['directory']}[DIR] Directory{COLORS['reset']}")
            if args.SHOW_IMAGES:
                print(f"{COLORS['image']}[IMAGE] Image file{COLORS['reset']}")
            if args.SHOW_TEXT:
                print(f"{COLORS['text']}[TEXT] Text file{COLORS['reset']}")
            if args.SHOW_OTHER:
                print(f"{COLORS['other']}[OTHER] Other file{COLORS['reset']}")
            print("-" * 50)
            
            print("\nFilesystem Tree:")
            for item in results:
                print(item)
                
            print(f"\nFound {len(results)} matching items")
            
    except Exception as e:
        print(f"Connection failed: {str(e)}")

if __name__ == "__main__":
    main()