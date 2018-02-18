import kivy, requests, bs4
kivy.require('1.10.0')

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.gesture import GestureDatabase, Gesture
from kivy.properties import ObjectProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button

Builder.load_file('what.kv')



class Root(RelativeLayout):
	
	# connect to host site for current day content 
	# download and store in variable
	page = requests.get('https://pxlmsufgaf.blogspot.co.uk/')
	soup = bs4.BeautifulSoup(page.text)
	content  = soup.select('#post-body-4778988161060613257')
	content = content[0].getText()
	source = soup.select('#post-body-1875809718724225559')
	source = source[0].getText()
	
	def __init__(self):
		super(Root, self).__init__()	
		
		self.ids.what_today_content.text = self.content
		self.ids.what_today_source.text = self.source



class WhatToday(App):
	def build(self):
		 return Root()


WhatToday().run()
