#!/usr/bin/python3

import requests, re, urllib3, argparse, os, logging, time, socket

try:
    from colorama import init
    init()
    R = '\033[0;31m'
    G = '\033[0;32m'
    B = '\033[0;34m'
    LR = '\033[1;31m'
    LC = '\033[1;36m'
except:
    pass
    R = ''
    G = ''
    B = ''
    LR = ''
    LC = ''

urllib3.disable_warnings()
session = requests.Session()
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"}
found_list = []
redirects_list = []
not_allowed_list = []
logging.basicConfig(filename='debug.log', level=logging.DEBUG)
terminal_size = os.get_terminal_size().columns

def checkRobots(url):
	r = session.get(url+'robots.txt', verify=False, headers=header)
	if r.status_code == requests.codes.ok:
		lines = r.text.splitlines()
		print(f'{LC}robots.txt Found Checking'.center(terminal_size))
		if re.search('admin|api|controll_panel|users|usarios|administrator|json|login|php|uploads|manager|dev|FCKEditor|old|db|private|members', r.text):
			for keyword in lines:
				if re.search('admin|api|controll_panel|users|usarios|administrator|json|login|php|uploads|manager|dev|FCKEditor|old|db|private|members', keyword):
					print(f'{G}Found {keyword}'.center(terminal_size))
				else:
					pass
		else:
			print(f'{LR}No interesting files found in robots.txt'.center(terminal_size))
	else:
		print(f'{R}\033[1m[!] Robots.txt was not found. [!]'.center(terminal_size))

def dirEnum(url, wordlist):
	try:
		print(f'{LC}\033[1mPlease Wait'.center(terminal_size))
		for link in open(wordlist).read().splitlines():
			print(f'Trying {url+link}'.center(terminal_size), end='\r\r')
			r = session.get(url+link, verify=False, timeout=5, headers=header, allow_redirects=False)
			if r.status_code == requests.codes.ok:
				found_list.append(url+link)
			elif r.status_code == requests.codes.temporary_redirect:
				redirects_list.append(url+link)
			elif r.status_code == requests.codes.unauthorized or r.status_code == requests.codes.not_acceptable:
				not_allowed_list.append(url+link)
			else:
				pass
	except requests.exceptions.ConnectionError:
		print(f'{R}[!!] Connection Error Please Check Your Internet. [!!]'.center(terminal_size))
		logging.critical('Internet is Down')
	except socket.gaierror:
		print(f'{LC}[!!] Something Happend Please Try Again. [!!]'.center(terminal_size))
		logging.error('Something Happend Bruh')
	except KeyboardInterrupt:
		logging.debug('You pressed Something while the script is running'.center(terminal_size))
		print(f'{R}[!!] Keyboard Interruption [!!]')
	except requests.exceptions.ReadTimeout:
		print(f'{LC}[!!] Timeout Error Please Try Increasing The Timeout [!!]'.center(terminal_size))
		logging.warning('Try Increasing The timeout')
	except requests.MaxRetryError:
		print(f'{LC}[!!] Max Retry Error Please Try Again. [!!]'.center(terminal_size))
		logging.error('Max Retry Error')		

def result(found_list, redirects_list, not_allowed_list):
	if(found_list != None or redirects_list != None or not_allowed_list != None):
		try:
			for dirs in found_list:
				print(f'{G}\033[1m{dirs}	Status:[200]')

			for dirs in not_allowed_list:
				print(f'{R}\033[1m{dirs}	Status:[400]')

			for dirs in redirects_list:
				print(f'{LC}\033[1m{dirs}	Status:[302]')
		except:
			pass
	else:
		print(f'{R}Nothing was found'.center(terminal_size))

def main():
	parser = argparse.ArgumentParser(description='Pyfuzzer is a Directory-Enumerator')
	parser.add_argument('-url', help='https://target.com/')
	parser.add_argument('-wordlist', help='/path/to/wordlist.txt')
	args = parser.parse_args()
	url = args.url
	if args.wordlist == None:
		wordlist = 'payload.txt'
	else:
		wordlist = args.wordlist

	if args.url is None:
		parser.print_help()
	else:
		try:
			print(f'{LR}Starting Script'.center(terminal_size))
			checkRobots(url)
			dirEnum(url, wordlist)
			print('\033[F', end='\033[K')
			result(found_list, not_allowed_list, redirects_list)
		except KeyboardInterrupt:
			logging.debug('You Pressed Something While The Script Is Running')
			print(f'{LR}[!!] Keyboard Interruption [!!]'.center(terminal_size))
		except requests.exceptions.MissingSchema:
			logging.error('Missing http Schema')
			print(f'{LC}[!!] Please Add https:// or http:// in your url [!!]'.center(terminal_size))
if __name__ == '__main__':
	main()
