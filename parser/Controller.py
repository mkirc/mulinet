import os
import subprocess
import xml.sax
#import mwparserfromhell
import logging
from os import listdir
from os.path import isfile, join
from classes import WikiXmlHandler
# from classes.Helper import prettify

class Controller:

    def __init__(self):

        # Logging 
        logging.basicConfig(
            # DEBUG INFO
            level=logging.DEBUG,
            format='%(levelname)s - %(message)s')

        self.log = logging.getLogger('mulietLogger')
        self.wikiData = self.loadWikiXml()
        self.langStr = None
        self.handler = None
        self.parser = None
        self.path = None

        # Input
        # for testing, create /muliet/testdata/in
    def loadWikiXml(self):
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
                # print(path + ' ' +'found')
        self.log.info('Input: %s files found.', len(currentFile))
        return currentFile

    def initializeHandler(self, path):

        self.path = path
        self.langStr = str(self.path.split('/')[-1].split('-')[0][:2])
        self.log.debug('Input: lang = %s', self.langStr)

        # Object for handling xml
        self.handler = WikiXmlHandler.WikiXmlHandler(self.langStr)

        # Parsing object
        self.parser = xml.sax.make_parser()
        self.parser.setContentHandler(self.handler)
        # Disable external entities / dtd requests
        self.parser.setFeature(xml.sax.handler.feature_external_ges, 0)
        self.log.info('Searching for words...')
        return

    def startHandler(self, limit):
        count = 0
        # print(self.path)
        for line in subprocess.Popen(['bzcat'],
                                 stdin = open(self.path),
                                 stdout = subprocess.PIPE).stdout:
            if count >= limit:
                break
            try:
                self.parser.feed(line)
            except StopIteration:
                break

            if self.handler._WikiItem:

                count += 1
                print(self.handler._WikiItem)
                self.handler._WikiItem = None

            # Stop when N Words have been found
            # if limit is not None and len(self.handler._WikiItems) >= limit:



                # for item in self.handler._WikiItem:

                #     # item.lang_dispatch()
                #     # item.find_stuff()

                #     self.log.debug('%s', item)
                #     # log.debug('%s', item.word['lang'])
                #     # log.debug('%s', item.word['title'])
                #     # log.debug('%s', item.word['phonetic'])
                #     # log.debug('%s', item.word['division'])
                #     # log.debug('%s', item.word['meaning'])
                #     # log.debug('%s', item.word['etymology'])
                #     # log.debug('%s', item.word['transl'])
                #     # log.debug('%s', item.word['refs'])

                # else:
                #     self.log.info('done!')
                # self.log.info(
                #     'Found %s words in %s pages', 
                #     len(self.handler._WikiItems), 
                #     self.handler._pageCount)

                # return self.handler._WikiItems



def main():

    c = Controller()
    c.initializeHandler(c.wikiData[0])
    c.startHandler(limit=2)

main()


# def run_shit(in_path, limit=None, save=True, outxml=False):
    
#     # Ugly test for language via title, fix that!
#     # utter crap

#     self.langStr = str(in_path.split('/')[-1].split('-')[0][:2])
#     log.debug('Input: lang = %s', langStr)

#     # Object for handling xml
#     handler = WikiXmlHandler.WikiXmlHandler(langStr)

#     # Parsing object
#     parser = xml.sax.make_parser()
#     parser.setContentHandler(handler)
#     # Disable external entities / dtd requests
#     parser.setFeature(xml.sax.handler.feature_external_ges, 0)
#     log.info('Searching for words...')

#     for line in subprocess.Popen(['bzcat'],
#                              stdin = open(in_path),
#                              stdout = subprocess.PIPE).stdout:
#         try:
#             parser.feed(line)
#         except StopIteration:
#             break


#         #linr
#         # Stop when N WordItems have been found
#         if limit is not None and len(handler._wiki_items) >= limit:

#             for item in handler._wiki_items:


                
#                 item.lang_dispatch()
#                 # item.find_stuff()

#                 log.info('%s', item)
#                 log.debug('%s', item.word['lang'])
#                 log.debug('%s', item.word['title'])
#                 log.debug('%s', item.word['phonetic'])
#                 log.debug('%s', item.word['division'])
#                 log.debug('%s', item.word['meaning'])
#                 log.debug('%s', item.word['etymology'])
#                 log.debug('%s', item.word['transl'])
#                 log.debug('%s', item.word['refs'])

#             # log.info('%s', handler._wiki_items[176].word['title'])
#             # log.info('%s', handler._wiki_items[176].word['meaning'])
#             else:
#                 log.info('done!')



#             log.info(
#                 'Found %s words in %s pages', 
#                 len(handler._wiki_items), 
#                 handler._page_count)


#             if save:

#                 out_dir = '/home/pedro/Hub/mewp/test-data/out/'

#                 if outxml:
#                     # save multiple files of a defined size 

#                     # set nums of words in outfile
#                     block_size = 100

#                     for count,item in enumerate(handler._wiki_items, start=1):

#                         item.find_stuff()
#                         a = count % block_size
#                         b = len(handler._wiki_items) - count
#                         if a <= block_size:
#                             # Pass words to XmlBuilder

#                             tree = XmlBuilder.build(
#                                                 str(item.word['title']),
#                                                 str(item.word['phonetic']),
#                                                 str(item.word['division']),
#                                                 str(item.word['meaning']),
#                                                 str(item.word['etymology']),
#                                                 str(item.word['transl']),
#                                                 str(item.word['refs']))
#                             if  a == 0:
#                                 # write out block as xml

#                                 name_str = 'test_n_' + str(limit) + '_p_' + str(count)
#                                 out_dir = out_dir + f'{name_str}.xml'
#                                 log.info('Saving xml...')
#                                 with open(out_dir, 'w') as fout:
#                                     fout.write(prettify(tree))
#                                     fout.close()

#                                     # Reset tree for new words
#                                     XmlBuilder.clear()
#                                     log.info('Saved block')
#                                     log.debug('Wrote to %s', out_dir)
#                             else:
#                                 if b == 0:
#                                 # write out remainder

#                                     name_str = name_str + '_r_' + str(count)
#                                     out_dir = out_dir + f'{name_str}.xml'
#                                     log.info('Saving xml...')
#                                     with open(out_dir, 'w') as fout:
#                                         fout.write(prettify(tree))
#                                         fout.close()

#                                         # Reset tree for ... hm.
#                                         XmlBuilder.clear()
#                                         log.info('Saved remaining words')
#                                         log.debug(
#                                             'Wrote remaining Words to %s', 
#                                             out_dir)
#                 elif sqlite:

#                     import sqlite3

#                     name_str = 'test_n_' + str(limit)
#                     out_dir = out_dir + f'{name_str}.db'                   
#                     conn = sqlite3.connect(out_dir)

#                     c = conn.cursor()
#                     log.info('Saving to db...')
#                     c.execute('''CREATE TABLE de_wiktionary 
#                                  (word_id INTEGER PRIMARY KEY,
#                                  title, 
#                                  phonetic, 
#                                  division, 
#                                  meaning, 
#                                  etymology, 
#                                  transl, 
#                                  refs)''')


                    
#                     for item in handler._wiki_items:
#                         word_tpl =  (   
#                                 str(item.word['title']),
#                                 str(item.word['phonetic']),
#                                 str(item.word['division']),
#                                 str(item.word['meaning']),
#                                 str(item.word['etymology']),
#                                 str(item.word['transl']),
#                                 str(item.word['refs']),
#                                     )


#                         c.execute("INSERT INTO de_wiktionary (title, phonetic, division, meaning, etymology, transl, refs) VALUES (?, ?, ?, ?, ?, ?, ?)", 
#                             word_tpl)

#                     for row in c.execute('SELECT word_id, title FROM de_wiktionary ORDER BY word_id'):
#                         log.debug(row)

#                     conn.commit()
#                     conn.close()
#                     log.info('Done.')









#             return handler._wiki_items





# run_shit(
#     wiki_data[1], 
#     limit=1, 
#     # save=True,
#     # sqlite=True
#     # outxml=True 
#     )

