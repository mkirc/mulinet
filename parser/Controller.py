import os
import subprocess
import xml.sax
#import mwparserfromhell
import logging
from os import listdir
from os.path import isfile, join
from classes import WikiXmlHandler
from classes.WikicodeProcessor import ProcessorFactory
from classes.WikiItem import WikiItem
from classes.XmlBuilder import XmlFactory

class Controller:

    def __init__(self):

        # Logging 
        logging.basicConfig(
            # DEBUG INFO
            level=logging.INFO,
            format='%(levelname)s - %(message)s')

        self.log = logging.getLogger('mulietLogger')

        self.wikiData = self.loadWikiXml()
        self.langStr = None
        self.handler = None
        self.parser = None
        self.path = None


    def loadWikiXml(self):

        # for testing, create /muliet/test-data/in        
        self.log.info('Hello again!')
        parentDir = os.path.dirname((os.path.dirname(__file__)))
        dataPath = os.path.join(parentDir, 'test-data/in/')
        files = [f for f in listdir(dataPath) if isfile(join(dataPath, f))]

        currentFile = []
        for file in files:
            path = dataPath + file
            if not os.path.exists(path):
                self.log.warning('No input files found.')
            else:
                currentFile.append(path)
                self.log.debug('%s found', path)
        self.log.debug('Input: %s files found.', len(currentFile))
        return currentFile

    def initializeHandler(self, inpath):

        self.path = inpath
        self.langStr = str(self.path.split('/')[-1].split('-')[0][:2])
        self.log.info('Input: lang = %s', self.langStr)

        # Object for handling xml
        self.handler = WikiXmlHandler.WikiXmlHandler(self.langStr)

        # Parsing object
        self.parser = xml.sax.make_parser()
        self.parser.setContentHandler(self.handler)
        # Disable external entities / dtd requests
        self.parser.setFeature(xml.sax.handler.feature_external_ges, 0)
        self.log.info('WikiXmlHandler initialized.')
        return

    def initializeProcessorFactory(self):

        self.pf = ProcessorFactory()
        self.pf.compileRegexbyLanguage(self.langStr)
        self.log.info('ProcessorFactory initialized.')
        return

    def initializeXmlFactory(self):

        self.xf = XmlFactory(self.langStr)
        self.log.info('XmlFactory initialized.')
        return

    def startFeed(self, limit):

        count = 0
        self.log.info('Starting Xml parsing.')        
        
        # start passing lines to xml handler
        for line in subprocess.Popen(['bzcat'],
                                 stdin = open(self.path),
                                 stdout = subprocess.PIPE).stdout:

            if count >= limit:
                self.log.info('Finished Xml parsing.')
                break
            try:
                self.parser.feed(line)
            except StopIteration:
                self.log.info('Finished Xml parsing.')
                break

            if self.handler._WikiItem:
                count += 1

                # postprocessing of WikiItem
                self.log.debug(self.handler._WikiItem)
                ppitem = self.processItem(self.handler._WikiItem)

                # build simple xml for db storage
                for item in ppitem:
                    outXml = self.buildXml(item, 'me', 'et', 'tr')
                    # outXml = self.buildXml(item, 'total')
                    for bloc in outXml:
                        self.log.info(bloc)


                # destroy _WikiItem
                self.handler._WikiItem = None


        self.log.info(
            'Found %s relevant Articles in %s pages', 
            count, 
            self.handler._pageCount)

    def buildXml(self, ppitem, *args):

        for m in args:
            if ppitem:
                tree = self.xf.spawnBuilder(m)
                if m == 'total':
                    tree.build(
                        ppitem.field['title'],
                        ppitem.field['phonetic'],
                        ppitem.field['meaning'],
                        ppitem.field['etymology'],
                        ppitem.field['transl']
                        )
                else:
                    ti = ppitem.field['title']
                    ot = None
                    if m == 'me':
                        ot = ppitem.field['meaning']
                    elif m == 'et':
                        ot = ppitem.field['etymology']
                    elif m == 'tr':
                        ot = ppitem.field['transl']
                    tree.build(ti, ot)
                yield tree.returnOutstr()  
                tree.clearBody()
        return

    def processItem(self, witem):
        
        # initialize PostProcessor
        self.pf.spawnProcessor()
        self.pf.loadWikiItem(witem)
        pp = self.pf.returnProcessor()
        
        # actual Processing
        pp.findIPA()
        pp.findEtymology()
        pp.findMeaning()
        pp.findTranslations()

        # out
        if pp.witem:

            yield pp.witem
            # display findings
            self.log.debug(pp.witem.field['phonetic'])
            self.log.debug(pp.witem.field['etymology'])
            self.log.debug(pp.witem.field['meaning'])
            self.log.debug(pp.witem.field['transl'])
            # if str(pp.witem) == 'Hallo':
            #     self.log.info(pp.witem.text)
            # else:
            #     pass
            
        # cleanup
        pp = None
        self.pf.destroyProcessor()
        return

    def writeOut(self):
        pass

def main():

    c = Controller()
    c.initializeHandler(c.wikiData[3])
    c.initializeProcessorFactory()
    c.initializeXmlFactory()
    c.startFeed(limit=1)

main()
