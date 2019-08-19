import re
import mwparserfromhell
# from classes.Helper import stringify

class WikiItem:
# Object for storing pages
	def __init__(self, lang, ti, text, wikicode):

		self.wikicode = wikicode
		self.text = text
		self.field = 	{ 

					'lang'		: 	lang,
					'title'     :   ti,
					'phonetic'  :   None,
					'division'  :   None,
					'meaning'   :   [],
					'etymology' :   None,
					'transl'    :   [],
					'refs'      :   None

						}
	def __str__(self):
		
		return self.field['title']

class WikiItemFactory:
	# Object for generating Words Objects
	def __init__(self):
		pass

	def returnWikiItem(self, lang, ti, text, wikicode):
		return WikiItem(lang, ti, text, wikicode)