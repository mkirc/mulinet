import re
import mwparserfromhell

class WikiItem:
# Object for storing pages / fields
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
	# Object for generating WikiItems
	def __init__(self):
		pass

	def returnWikiItem(self, lang, ti, text, wikicode):
		return WikiItem(lang, ti, text, wikicode)