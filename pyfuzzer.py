import requests, re, urllib3, argparse, os
import socket
from anytree import Node, RenderTree
import logging

urllib3.disable_warnings()
session = requests.Session()
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"}
found_list = []
redirects_list = []
not_allowed_list = []
not_found_list = []
logging.basicConfig(filename='debug.log', level=logging.DEBUG)

def checkRobots(url):
	r = session.get(url+'robots.txt', verify=False)
	if r.status_code == requests.codes.ok:
		lines = r.text.splitlines()
		for keyword in lines:
			if re.search('admin|api|controll_panel|users|usarios|administrator|json|login|php|uploads|manager|dev|FCKEditor|old|db|private|members', keyword):
				print(f'Found {keyword}')
			else:
				pass
	else:
		print('[!] Robots.txt was not found. [!]')

def dirEnum(url, wordlist):
	try:
		for link in open(wordlist).read().splitlines():
			print('[!] Please Wait.... [!]', end='\r')
			r = session.get(url+link, verify=False, timeout=5, headers=header)
			if r.status_code == requests.codes.ok:
				found_list.append(url+link)
			elif r.status_code == requests.codes.temporary_redirect:
				redirects_list.append(url+link)
			elif r.status_code == requests.codes.unauthorized or r.status_code == requests.codes.not_acceptable:
				not_allowed_list.append(url+link)
			else:
				not_found_list.append(url+link)
	except ConnectionError:
		logging.critical('Internet is Down')
		print('[!!] Connection Error Please Check Your Internet. [!!]')
	except socket.gaierror:
		logging.error('Something Happend Bruh')
		print('[!!] Something Happend Please Try Again. [!!]')
	except KeyboardInterrupt:
		logging.debug('You pressed Something while the script is running')
		print('[!!] Keyboard Interruption [!!]')
	except requests.exceptions.ReadTimeout:
		logging.warning('Try Increasing The timeout')
		print('[!!] Timeout Error Please Try Increasing The Timeout [!!]')

def _tree(found_list, redirects_list, not_allowed_list, not_found_list):
	not_found = Node('[!] Not Found Directories [!]')
	for url in not_found_list:
		found_url = Node(url, parent=not_found)
	for pre,fill,node in RenderTree(not_found):
		print(f'{pre}{node.name}')

	found = Node('[+] Found Directories [+]')
	for url in found_list:
		found_url = Node(url, parent=found)
	for pre,fill,node in RenderTree(found):
		print(f'{pre}{node.name}')

	not_allowed = Node('[!] Not Found Directories [!]')
	for url in not_allowed_list:
		found_url = Node(url, parent=not_allowed)
	for pre,fill,node in RenderTree(not_allowed):
		print(f'{pre}{node.name}')

	redirects = Node('[!] Redirecting Directories [!]')
	for url in redirects_list:
		found_url = Node(url, parent=redirects)
	for pre,fill,node in RenderTree(redirects):
		print(f'{pre}{node.name}')

def main():
	parser = argparse.ArgumentParser(description='Pyfuzzer is a Directory-Enumerator')
	parser.add_argument('-url', help='https://target.com/')
	parser.add_argument('-wordlist', help='/path/to/wordlist.txt')
	args = parser.parse_args()
	url = args.url
	if args.wordlist == None:
		wordlist = 'payload.txt'.format(os.getcwd())
	else:
		wordlist = args.wordlist

	if args.url is None:
		parser.print_help()
	else:
		print('[!] Starting Script! [!]', end='\n')
		checkRobots(url)
		dirEnum(url, wordlist)
		_tree(found_list, not_found_list, not_allowed_list, redirects_list)

if __name__ == '__main__':
	main()
