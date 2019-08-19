import xml.sax
import mwparserfromhell
from classes.WikiItem import WikiItem, WikiItemFactory



class WikiXmlHandler(xml.sax.handler.ContentHandler):
    # Content Handler, inherited from sax
    def __init__(self, langStr):
        xml.sax.handler.ContentHandler.__init__(self)
        self._buffer = None
        self._values = {}
        self._current_tag = None
        self._pages = []
        self._pageCount = 0
        self._WikiItem = None
        self._lang = langStr


    def characters(self, content):
        # Chars between opening and closing tag
        if self._current_tag:
            self._buffer.append(content)

    def startElement(self, name, attrs):
        # Opening tag of element
        if name in ('title', 'text'):
            self._current_tag = name
            self._buffer = []

    def endElement(self, name):
        # Closing tag of element
        if name == self._current_tag:
            self._values[name] = ' '.join(self._buffer)

        if name == 'page':
            self._pageCount += 1
            self._pages.append((self._values['title'], self._values['text']))

            ap = ArticleProcessor()
            word = ap.processArticle(
                                    self._values['title'], 
                                    self._values['text'], 
                                    template = ap.getTemplatebyLanguage(self._lang)
                                    )
            if word:
                # Check for internal pages (eg. Mediawiki:Helppage)
                if not ':' in word['title']:
                    wf = WikiItemFactory()
                    self._WikiItem = (wf.returnWikiItem(
                                                            self._lang,
                                                            word['title'],
                                                            word['text'],
                                                            word['wikicode']
                                                            )
                                            ) 

class ArticleProcessor:

    def __init__(self):
        self.wikicode = None
        self.matches = None

    def processArticle(self, title, text, template):
    # Process a wikipedia article looking for template
        
        # Create a parsing object
        wikicode = mwparserfromhell.parse(text)
        
        # Search through templates for the template
        matches = wikicode.filter_templates(matches = template)
        
        if len(matches) >= 1:

            return {'title' : title,
                    'text' : text, 
                    'wikicode' : wikicode}

    def getTemplatebyLanguage(self, lang):

        if lang == 'de':
            template = 'Bedeutungen'
        elif lang == 'en':
            template = 'Etymology'
        else:
            template = None
        return template

