#!/usr/bin/python
# -*- coding: UTF-8 -*-

import httplib2
import sys
import json
import curses
import contextlib
import subprocess
import os
import ConfigParser
from apiclient import discovery

# Constant curses color_pair names. Names prefixed with
# B_ are bold.
DEFAULT 	= 1
TITLE 		= 2
LINK 		= 3
SNIPPET 	= 4
B_TITLE 	= 5
B_LINK  	= 6
B_SNIPPET 	= 7

CONFIG_PATH = os.path.expanduser("~/.config/ggl/ggl.config")


@contextlib.contextmanager
def curses_screen():
    try:
        screen=curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        try: 
			curses.start_color()
			curses.init_pair(DEFAULT, curses.COLOR_BLACK, curses.COLOR_WHITE)

			curses.init_pair(TITLE, 	curses.COLOR_RED, 	curses.COLOR_WHITE)
			curses.init_pair(LINK, 		curses.COLOR_BLUE, 	curses.COLOR_WHITE)
			curses.init_pair(SNIPPET, 	curses.COLOR_BLACK, curses.COLOR_WHITE)

			curses.init_pair(B_TITLE, 	curses.COLOR_BLACK, curses.COLOR_WHITE)
			curses.init_pair(B_LINK, 	curses.COLOR_BLACK, curses.COLOR_WHITE)
			curses.init_pair(B_SNIPPET, curses.COLOR_BLACK, curses.COLOR_WHITE)

			screen.bkgd(curses.color_pair(DEFAULT))
			screen.border(0)
        except: 
        	print "Color errors"

        yield screen
    finally:
        screen.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()


class ggl_ui:
	def __init__(self, searchResult, config):
		self.json = searchResult
		self.selected = 0
		self.screen = curses_screen()
		self.config = config

	def ui_loop(self):
		input = 0
		self.selected = 0

		with curses_screen() as scr:
			self.screen = scr
			count = self.ui_redraw()

			# The indices grows downwards
			while input != "q":
				input = self.screen.getkey()
				if input == "j":
					if self.selected+1 < count:
						self.selected += 1
						self.ui_redraw()
				elif input == "k":
					if self.selected > 0:
						self.selected -= 1
						self.ui_redraw()
				elif input == "o":
					run_cmd(self.json, self.selected, self.config)
					if input == "\n":
						return

	def ui_redraw(self):
		height = self.screen.getmaxyx()[0]
		width = self.screen.getmaxyx()[1]
		if height < 10 or width < 20:
			print "Run ggl in a human sized tty please."
			return

		line = 1
		count = 0
		for res in self.json["items"]:
			if line + 5 >= height:
				break
			is_sel = (self.selected == count)
			self._print(5, line+1, width-10, res["title"], 			TITLE, 	 is_sel)
			self._print(5, line+2, width-10, res["formattedUrl"], 	LINK, 	 is_sel)
			self._print(5, line+3, width-10, res["snippet"], 		SNIPPET, is_sel)
			line += 5
			count+= 1

		self.screen.refresh()
		return count

	def _print(self, x, y, w, str, type, sel):
		bold = 0
		if sel:
			type += 3
			bold = curses.A_BOLD
		t = curses.color_pair(type)
		self.screen.addstr(y, x, printable_str(str, w), t | bold)

class ggl_config:
	def __init__(self):
		self.cfg = ConfigParser.ConfigParser()
		if len(self.cfg.read(CONFIG_PATH)) == 0:
			print "Unable to open ", CONFIG_PATH
			exit()

		self.assert_config("api", "api_key")
		self.assert_config("api", "search_engine")
		self.assert_config("cmd", "open_url_cmd")

	def assert_config(self, section, opt):
		cfglen = 0
		try:
			cfglen = len(self.cfg.get(section, opt).strip())
		except:
			# If the option is undefined, an exception is raised
			cfglen = 0

		if cfglen == 0:
			print "Option ["+section+"] "+opt+" is required. See README.md and update '%s'" % CONFIG_PATH
			exit()

	def get(self, section, opt, default=""):
		value = default
		try:	
			value = self.cfg.get(section, opt)
			if len(value) == 0:
				value = default
		except:	
			pass

		return value

def printable_str(str, maxlen):
	"""
	Remove all newlines and cut the string
	off after "maxlen" characters. The string
	is also re-encoded in UTF-8.
	"""
	str = str.encode("utf8").strip()

	str = str.replace("\n", " ")
	if len(str) > maxlen-6:
		str = str[:maxlen-6]
		str = str + "..."

	return str

def log(str):
	# TODO: Enable logging
	pass #os.system("echo \""+str+"\" >> ggl.log")


def get_cmd_redirect(config):
	# Returns on the form:
	# " >/dest/file 2>&1 "
	redirect = " >" 
	redirect += config.get("cmd", "cmd_out_redirect", "/dev/null") 
	redirect += " 2>&1 "
	return redirect

def get_cmd(j, sel, config):
	# The http:// is absolutely necessary 
	link = j["items"][sel]["link"]
	if link[:4] != "http":
		link = "http://" + link

	

	cmd =  config.get("cmd", "open_url_cmd") + " "
	cmd += link
	cmd += get_cmd_redirect(config)

	log("cmd: " + cmd)
	return cmd

def run_cmd(j, sel, config):
	cmd = get_cmd(j, sel, config)
	os.system(cmd)

	posturl = config.get("cmd", "post_cmd")
	if len(posturl):
		os.system(posturl + get_cmd_redirect(config))



def dummysearch():
	f = open("dummy", "r")
	return json.loads(f.read())

def main(argv):
	config = ggl_config()

	service = discovery.build('customsearch', 'v1',	developerKey=config.get("api", "api_key"))

	j = service.cse().list(q=argv[1], cx=config.get("api", "search_engine")).execute()
	#j = dummysearch()
	assert(type(j) == dict)

	if int(j["searchInformation"]["totalResults"]) == 0:
		print "No results."
		exit()

	ui = ggl_ui(j, config)
	ui.ui_loop()


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "Search term required"
		exit()
	
	# Concat all arguments onto argv[1], deal with it, etc
	for i in range(2,len(sys.argv)):
		sys.argv[1] += " " + sys.argv[i]
	sys.argv[1] = sys.argv[1].decode("utf8")

	main(sys.argv)
 
