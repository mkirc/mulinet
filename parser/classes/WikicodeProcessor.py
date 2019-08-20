from WikiItem import WikiItem

class PostProcessor:
	def __init__(self, witem):

		self.wItem = witem
		self.raw = witem.text
		self.wcode = witem.wikicode

	# def find_en_stuff(self):

	# 	cont = self.wikicode.filter_text()

	# 	body = re.sub('<.*?>', '', self.text.replace("\n", ''))
	# 	# print(body)
	# 	# etym = self.wikicode.filter(matches='===Etymology [0-9+]===')

	# 	# find IPA - pronounciation
	# 	if 'IPA' in body:
	# 		try:
	# 			self.word['phonetic'] = self.wikicode.filter_templates(matches='IPA')[0].params[0]			
	# 		except IndexError:
	# 			pass
	# 	else:
	# 		pass


	# 	# print(self.word['phonetic'])

	# 	et = re.compile('===Etymology [0-9+]===\s(.+?)(?=={3,})')
	# 	me = re.compile('====Noun====\s(.+?)(?=={3,})')
	# 	_it = re.compile('#[\*:\s](.+?)(?=#)')

	# 	try:
	# 		# self.word['meaning'] = '\n'.join(re.findall(_it, ''.join(re.findall(me, body))))
	# 		for r in re.findall(_it, ''.join(re.findall(me, body))):
	# 			self.word['meaning'].append(r)
	# 		# self.word['meaning'] = '\n'.join(re.findall(_it, re.findall(me, body)[0]))
	# 		# self.word['meaning' = re.sub('{{.*?}}', '' ,self.word['meaning'].strip())
	# 		# print(self.word['meaning'])
	# 	except IndexError:
	# 		pass
	# 	for m in self.word['meaning']:
	# 		m = re.sub('{{.*?}}', '' ,m.strip())

	# 	if 'Etymology' in body:
	# 		try:
	# 			self.word['etymology'] = '\n'.join(re.findall(et, body))
	# 			# print(self.word['etymology'])
	# 		except IndexError:
	# 			pass
	# 	else:
	# 		pass

	# def find_de_stuff(self):
	# 	# cant use mwparserfromhell b/c formatting hell
	# 	# so i fell back on writing the regexes myself

	# 	# generate text as list
	# 	cont = self.wikicode.filter_text()

	# 	# prep text for regex processing
	# 	body = re.sub('[=:]', '', self.text.replace("\n",'').strip(':  '))
		

	# 	# compile regexes
	# 	me = re.compile('{{Bedeutungen}}\s+(.+?)(?={{Herkunft}}|{{Synonyme}}|{{Beispiele}}|{{Entlehnungen}}|{{Abkürzungen}})')
	# 	et = re.compile('{{Herkunft}}\s+(.+?)(?={{Synonyme}}|{{Beispiele}})')
	# 	di = re.compile('{{Worttrennung}}\s+(.+?)(?={{Aussprache}}|{{Bedeutungen}})')
	# 	rf = re.compile('{{Referenzen}}\s+(.+?)(?={{Quellen}})')

	# 	# find attrs
	# 	try:
	# 		# self.word['meaning'] = re.search('Bedeutungen (.+?)(?=Beispiele|Synonyme|Herkunft|Entlehnungen|Abkürzungen)', body).group(1)			
	# 		self.word['meaning'] = re.findall(me, body)[0]
	# 	except IndexError:
	# 	# except AttributeError:
	# 		pass
	# 	try:
	# 		self.word['etymology'] = re.findall(et, body)[0]
	# 	except IndexError:
	# 		pass  	 
	# 	try:
	# 		self.word['division'] = re.findall(di, body)[0]
	# 	except IndexError:
	# 		pass
	# 	try:
	# 		self.word['refs'] = re.findall(rf, body)[0]
	# 	except IndexError:
	# 		pass

		
	# 	# find IPA - pronounciation
	# 	if 'Lautschrift' in body:
	# 		try:
	# 			self.word['phonetic'] = self.wikicode.filter_templates(matches='Lautschrift')[0].params[0]			
	# 		except IndexError:
	# 			pass
	# 	else:
	# 		pass

	# 	# Find available translations 
	# 	if 'Ü-Tabelle' in body:
	# 		tr = re.compile('{{(.+?)(?=}})')
	# 		try:
	# 			ltr = str(self.wikicode.filter_templates(matches='Ü-Tabelle')[0])
	# 			self.word['transl'] = ', '.join([i for i in re.findall(tr, ltr)])
	# 		except ValueError:
	# 			pass
	# 	else:
	# 		pass

	# 	# find references if re method fails
	# 	if self.word['refs'] is None:
	# 		if 'Referenzen' in body:
	# 			try:
	# 				self.word['refs'] = cont[cont.index('Referenzen') + 1:cont.index('Quellen')]
	# 			except ValueError:
	# 				pass
	# 		else:
	# 			pass
	# 	else:
	# 		pass

	# def lang_dispatch(self):
	# 	# sets postprocessing function based
	# 	# on language

	# 	if self.word['lang'] == 'de':
	# 		self.find_de_stuff()
	# 	elif self.word['lang'] == 'en':
	# 		self.find_en_stuff()
	# 	else:
	# 		pass

	
# def prettify(elem):
#     # Return a pretty-printed XML string for the Element.

#     rough_string = ElementTree.tostring(elem, 'utf-8')
#     reparsed = minidom.parseString(rough_string)
  
#     return reparsed.toprettyxml(indent="  ")



# def stringify(in_lis):
# 	# Clean input list of newlines, unwanted whitepace and empty items
# 	# Return string
	
# 	in_lis = [i.replace("\n", "").strip(':  ') for i in in_lis]
# 	# in_lis = map(lambda l: l.replace("\n", "").strip(), in_lis)
# 	in_lis = list(filter(None, in_lis))
# 	out_str = ' '.join(in_lis)



# 	# Test for ml-tags, remove them

# 	# if '<' or '>' in in_str:
# 	# 	cleanr = re.compile('<.*?>')
# 	# 	out_str = re.sub(cleanr, '', out_str)
# 	# else:
# 	# 	pass

# 	return out_str
	