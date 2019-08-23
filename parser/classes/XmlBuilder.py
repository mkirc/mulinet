from xml.dom import minidom
import xml.etree.ElementTree as ET                                                                                                                                                    
from xml.etree.ElementTree import Element, SubElement, Comment, tostring


class XmlBuilder:
	
	def __init__(self, langStr):
		self.root = Element('root')
		self.head = SubElement(self.root, 'head')
		self.head.append(Comment(str(langStr) + '-wiktikonary'))
		self.body = SubElement(self.root, 'body')
		self.outStr = None

	def prettifyXml(self, elem):

	    # Return a pretty-printed XML string for the Element.
	    rough_string = ET.tostring(elem, encoding='utf-8')
	    reparsed = minidom.parseString(rough_string)

	    return reparsed.toprettyxml(indent="  ")

	def returnOutstr(self):

		return self.prettifyXml(self.root)

	def returnRoot(self):

		return self.root

	def clearBody(self):

		self.body.clear()
		return

class TotalBuilder(XmlBuilder):

	def build(self, ti, ph, me, et, tr):

		self.word = SubElement(self.body, 'word')
		self.node = SubElement(self.word, 'title')
		self.node.text = str(ti)

		self.node = SubElement(self.word, 'phonetic')
		self.node.text = str(ph)

		self.node = SubElement(self.word, 'meaning')

		try:
			for k,v in me.items():
				nodeStr = 'me-' + str(k)
				self.meNode = SubElement(self.node, nodeStr)
				self.meNode.text = str(me[k])
		except KeyError:
			pass

		self.node = SubElement(self.word, 'etymology')
		
		try:
			for count,e in enumerate(et):
				nodeStr = 'et-' + str(count + 1)
				self.etNode = SubElement(self.node, nodeStr)
				self.etNode.text = str(e)
		except IndexError:
			pass


		self.node = SubElement(self.word, 'translation')
		try:
			for count,t in enumerate(tr):
				nodeStr = 'tr-' + str(count)
				self.trNode = SubElement(self.node, nodeStr)
				self.trNode.text = str(t)
		except IndexError:
			pass

		return

class MeBuilder(XmlBuilder):

	def build(self, ti, me):
		self.word = SubElement(self.body, 'word')
		self.node = SubElement(self.word, 'title')
		self.node.text = str(ti)

		self.node = SubElement(self.word, 'meaning')

		try:
			for k,v in me.items():
				nodeStr = 'me-' + str(k)
				self.meNode = SubElement(self.node, nodeStr)
				self.meNode.text = str(me[k])
		except KeyError:
			pass

		return

class EtBuilder(XmlBuilder):

	def build(self, ti, et):
		self.word = SubElement(self.body, 'word')
		self.node = SubElement(self.word, 'title')
		self.node.text = str(ti)
		self.node = SubElement(self.word, 'etymology')
		
		try:
			for count,e in enumerate(et):
				nodeStr = 'et-' + str(count + 1)
				self.etNode = SubElement(self.node, nodeStr)
				self.etNode.text = str(e)
		except IndexError:
			pass
		return

class TrBuilder(XmlBuilder):

	def build(self, ti, tr):
		self.word = SubElement(self.body, 'word')
		self.node = SubElement(self.word, 'title')
		self.node.text = str(ti)
		self.node = SubElement(self.word, 'translation')
		try:
			for count,t in enumerate(tr):
				nodeStr = 'tr-' + str(count)
				self.trNode = SubElement(self.node, nodeStr)
				self.trNode.text = str(t)
		except IndexError:
			pass

		return

class XmlFactory:

	def __init__(self, langStr):

		self.langStr = langStr
		self.builder = None

	def setBuilder(self, mod='total'):

		if mod == 'total':
			self.builder = TotalBuilder(self.langStr)
		elif mod == 'me':
			self.builder = MeBuilder(self.langStr)
		elif mod == 'et':
			self.builder = EtBuilder(self.langStr)
		elif mod == 'tr':
			self.builder = TrBuilder(self.langStr)
		return

	def spawnBuilder(self, mod):

		self.setBuilder(mod)
		return self.builder 
