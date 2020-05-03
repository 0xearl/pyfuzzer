import requests
import re
import urllib3
from socket import gethostbyname, gaierror
from anytree import Node, RenderTree
import argparse
import os
urllib3.disable_warnings()
s = requests.Session()
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"}
found_list = []
redirects_list = []
not_allowed_list = []
not_found_list = []
class fuzz():
	  parser = argparse.ArgumentParser()
	  parser.add_argument('-url', help='https://target.com')
	  parser.add_argument('-wordlist', help='custom wordlist ex: /path/to/wordlist.txt')
	  args = parser.parse_args()
	  url = args.url
	  if args.wordlist == None:
	  	wordlist = '{}\\payload.txt'.format(os.getcwd())
	  else:
	  	wordlist = args.wordlist
	  def checkRobots(url):
	   	r = s.get(url+"robots.txt", verify=False, timeout=5, headers=header)
	   	if r.status_code == requests.codes.ok:
	   		lines = r.text.splitlines()
	   		for keyword in lines:
	   			if re.search('admin|api|controll_panel|users|usarios|administrator|json|login|php|uploads|manager|dev|FCKEditor|old|db|private|members', keyword):
	   				print(keyword)
	   			else:
	   				pass
	   	else:
	   		print("Robots.txt wasn't found proceeding to bruteforcing files/dirs")
	   		pass
	  def dirhunt(url, wordlist):
	  	try:
	  		for link in open(wordlist).read().splitlines():
	  			print("Please Wait..", end='\r')
		  		r = s.get(url+link, verify=False, timeout=5, headers=header)
		  		if r.status_code == requests.codes.ok:
		  			found_list.append(url+link)
		  		elif r.status_code == requests.codes.temporary_redirect:
		  			redirects_list.append(url+link)
		  		elif r.status_code == requests.codes.unauthorized or r.status_code == requests.codes.not_acceptable:
		  			not_allowed_list.append(url+link)
		  		else:
		  			not_found_list.append(url+link)
	  	except ConnectionError:
	  		print("Check Your Internet!..")
	  		pass
	  	except KeyboardInterrupt:
	  		print('Keyboard Interruption script Halted')
	  		pass
	  	except gaierror:
	  		print('Please Retry Again.')
	  def _tree(found_list, redirects_list, not_allowed_list, not_found_list):
	  	not_found = Node('Not Found')
	  	for url in not_found_list:
	  		found_url = Node(url, parent=not_found)
	  	for pre, fill, node in RenderTree(not_found):
	  		print('%s%s' % (pre, node.name))
	  	found = Node('Found')
	  	not_allowed = Node('Not Allowed')
	  	for url in not_allowed_list:
	  		found_url = Node(url, parent=not_allowed)
	  	for pre, fill, node in RenderTree(not_allowed):
	  		print('%s%s' % (pre, node.name))
	  	redirects = Node('Redirects')
	  	for url in redirects_list:
	  		found_url = Node(url, parent=redirects)
	  	for pre, fill, node in RenderTree(redirects):
	  		print('%s%s' % (pre, node.name))
	  	for url in found_list:
	  		found_url = Node(url, parent=found)
	  	for pre, fill, node in RenderTree(found):
	  		print('%s%s' % (pre, node.name))
	  checkRobots(url)
	  dirhunt(url, wordlist)
	  print('\n')
	  _tree(found_list, redirects_list, not_allowed_list, not_found_list)

if __name__ == '__main__':
	fuzz()
