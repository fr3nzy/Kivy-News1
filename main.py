import kivy
kivy.require('1.10.0')

from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', False)

import kivy, requests, bs4, webbrowser, xerox, os
from time	import strftime, localtime

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.gesture import GestureDatabase, Gesture
from kivy.core.clipboard import Clipboard
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
from kivy.uix.button import Button


Builder.load_file('what.kv')

class Logic:
	# dependent on width of window, create seperator of hyphens
	width_win = int(Window.size[0] - ((Window.size[0] / 10) * 7.65) )
	l = []
	for i in range(0, width_win):
		l.append('-')
	separator = ''.join(l)

	# connect to host site for current day content 
	# download and store in variable
	page = requests.get('https://pxlmsufgaf.blogspot.co.uk/')
	soup = bs4.BeautifulSoup(page.text)
	content  = soup.select('#post-body-4778988161060613257')
	content = content[0].getText()
	source = soup.select('#post-body-1875809718724225559')
	source = source[0].getText()
	
	# check current files for data. if False write data to current files
	# if True move current file data to folder and write new data to current files
	cwd = os.getcwd()
	with open('data/content', 'r') as f:
		data = f.read()
	if data not in content:
		if os.stat('data/content').st_size > 0: #file is not empty?
			with open('data/date', 'r') as f:
				date = f.read()
			try:
				os.mkdir('data/' + date) #foldername = date
			except Exception:
				pass
			os.chdir('data/' + date)
			with open('content', 'w') as f:
				f.write(data)
			with open('sources', 'w') as f:
				f.write(source)
			with open('date', 'w') as f:
				f.write(date)
		os.chdir(cwd)
		with open('data/content', 'w') as f:
			f.write(content)
		with open('data/sources', 'w') as f:
			f.write(source)
		with open('data/date', 'w') as f:
			f.write(strftime('%d-%m-%y', localtime())) # date for current day
	
	# separate links from <source> and store in list <sources>
	sources = []
	n = 0
	for counter, item in enumerate(source):
		if item==' ':
			if n > 0:
				x = 0
				for i in enumerate(sources):
					x += len(sources[i[0]])
				counter -= x	
			sources.append(source[0:counter+1])
			source = source[counter+1:len(source)]
			n += 1
		
			
class CopyButton(Button, Logic):
	def on_press(self):
		try:	# copy to clipboard
			xerox.copy(Logic.sources[(int(url_no) - 1)])
		except Exception as e:
			print(e)


class OpenButton(Button, Logic):
	def on_press(self):
		try:
			webbrowser.open(Logic.sources[(int(url_no) - 1)]) # list item 1 = 0
		except Exception as e:
			print(e)	

	
class Root(RelativeLayout, Logic):
	def __init__(self):
		super(Root, self).__init__()	
		
		self.content = Logic.content
		self.separator = Logic.separator
		
		self.ids.date.text = strftime('%a %d/%m %Y', localtime())
		self.ids.seperator_current.text = '\n\n\n\n' + self.separator
		self.ids.what_today_content.text = self.content
		
		self.ids.previous.text = 'Previously viewed'
		self.ids.separator_articles.text = '\n\n\n\n' + self.separator
		
		
	def input_text(self, value):
		global url_no
		url_no = value
		

class WhatToday(App):
	def build(self):
		return Root()
		 


WhatToday().run()
