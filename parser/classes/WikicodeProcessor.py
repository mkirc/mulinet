import re
import mwparserfromhell
# from WikiItem import WikiItem

class PostProcessor:
    def __init__(self, regex):

        self.witem = None
        # self.out = None
        self.raw = None
        self.wcode = None
        self.regex = regex

class EnPostProcessor(PostProcessor):

    def findIPA(self):

        if 'IPA' in self.raw:
            try:
                ipa = self.wcode.filter_templates(matches='IPA')[0].params[0]
                self.witem.field['phonetic'] = ipa       
            except IndexError:
                pass



    def findEtymology(self):

        if 'Etymology' in self.raw:
            try:
                for e in re.findall(self.regex['et'], self.raw):
                    for f in re.findall(self.regex['nlIt'], e):
                        # filter two-or-more whitespaces
                        x = re.sub('\s{2,}','', f)
                        # filter unicode characters, leading whitespace
                        x = x.encode('ascii', 'ignore').decode().strip()
                        # filter html
                        x = re.sub('<.*>','', x)
                        if x:
                            self.witem.field['etymology'].append(x)
                # self.out['etymology'] = '\n'.join(re.findall(self.regex['et'], self.body))
            except IndexError:
                pass
        return

    def findMeaning(self):

        # this sounds too philosphical
       
        try:
            nouns = []
            verbs = []
            adjectives = []
            me = {}
            # iterate over each match/conditional
            for r in re.findall(self.regex['me'], self.raw):
                if r[0] == 'Noun':
                    nouns.append(r[1])
                if r[0] == 'Verb':
                    verbs.append(r[1])
                if r[0] == 'Adjective':
                    adjectives.append(r[1])
                # print(me)
            me['Nouns'] = ''.join(nouns)
            me['Verbs'] = ''.join(verbs)
            me['Adjectives'] = ''.join(adjectives)

            for k, v in me.items():
                current = []
                # iterate over each number(denoted by #)
                for m in re.findall(self.regex['meIt'], me[k]):
                    # filter chars enclosed by {}
                    m = re.sub('{{.*?}}', '' , m)
                    # filter html
                    m = re.sub('<.*>','', m)
                    # filter unicode characters, leading whitespace
                    m = m.encode('ascii', 'ignore').decode().strip()
                    if m:
                        current.append(m)
                self.witem.field['meaning'][k] = current
        except IndexError:
            pass
        return

    def findTranslations(self):

        if 'Translations' in self.raw:
            try:
                for tr in re.findall(self.regex['tr'], self.raw):
                    for line in re.findall(self.regex['trIt'], tr):
                        self.witem.field['transl'].append(line)
            except IndexError:
                pass
        return

    def findReferences(self):
        pass


class DePostProcessor(PostProcessor):

    def findIPA(self):
        # find IPA - pronounciation
        if 'Lautschrift' in self.raw:
            try:
                ipa = self.wcode.filter_templates(matches='Lautschrift')[0].params[0]
                self.witem.field['phonetic'] = ipa          
            except IndexError:
                pass
        #   try:
        #       self.word['division'] = re.findall(di, body)[0]
        #   except IndexError:
        #       pass
        return

    def findMeaning(self):

        current = []
        try:
            for m in re.findall(self.regex['me'], self.body):
                current.append(m)
            # self.word['meaning'] = re.findall(me, body)[0]
        except IndexError:
            pass
        if current:
            for i in range(len(current)):
                self.witem.field['meaning'][i + 1] = current[i]
        return        

    def findEtymology(self):

        try:
            for e in re.findall(self.regex['et'], self.body):
                self.witem.field['etymology'].append(e)
            # self.word['etymology'] = re.findall(et, body)[0]
        except IndexError:
            pass
        return     

    def findTranslations(self):

        # Find available translations 
        if 'Ü-Tabelle' in self.body:
            try:
                ltr = str(self.wcode.filter_templates(matches='Ü-Tabelle')[0])
                self.witem.field['transl'] = ', '.join([i for i in re.findall(self.regex['tr'], ltr)])
            except ValueError:
                pass
        return

    def findReferences(self):

        try:
            self.witem.field['refs'] = re.findall(rf, self.body)[0]
        except IndexError:
            pass
        # find references if re method fails
        if self.witem.field['refs'] is None:
            if 'Referenzen' in self.body:
                try:
                    self.witem.field['refs'] = cont[cont.index('Referenzen') + 1:cont.index('Quellen')]
                except ValueError:
                    pass
        return

class ProcessorFactory:

    def __init__(self):

        self.langStr = None
        self.pp = None
        self.regex = {}

    def compileRegexbyLanguage(self, langStr):
        
        self.langStr = langStr

        if self.langStr == 'en':
            self.regex = self.compileEnRegex()

        elif self.langStr == 'de':
            self.regex = self.compileDeRegex()

        return      

    def compileEnRegex(self):
            regex = {}
            # passages
            regex['et'] = re.compile('=={2,}Etymology [0-9+]=={2,}(.+?)(?=={2,})', re.DOTALL)
            regex['me'] = re.compile('=={2,}(Noun|Verb)=={2,}(.+?)(?=={2,})', re.DOTALL)
            regex['tr'] = re.compile('=={2,}Translations=={2,}(.+?)(?=={2,})', re.DOTALL)
            # iterators
            regex['nlIt'] = re.compile('(.+?)(?=\n)')
            regex['meIt'] = re.compile('#{1,2}\s(.+?)(?=\n)')
            regex['trIt'] = re.compile('\*{1,2}\s(.+?)(?=\n)')

            return regex

    def compileDeRegex(self):

            regex = {}
            regex['me'] = re.compile('{{Bedeutungen}}\s+(.+?)(?={{Herkunft}}|{{Synonyme}}|{{Beispiele}}|{{Entlehnungen}}|{{Abkürzungen}})')
            regex['et'] = re.compile('{{Herkunft}}\s+(.+?)(?={{Synonyme}}|{{Beispiele}})')
            regex['tr']= re.compile('{{(.+?)(?=}})')
            regex['di'] = re.compile('{{Worttrennung}}\s+(.+?)(?={{Aussprache}}|{{Bedeutungen}})')
            regex['rf'] = re.compile('{{Referenzen}}\s+(.+?)(?={{Quellen}})')
            return regex        

    def spawnProcessor(self):

        if self.langStr == 'en':
            self.pp = EnPostProcessor(self.regex)
        if self.langStr == 'de':
            self.pp = DePostProcessor(self.regex)


        # self.pp = PostProcessor(self.regex)
        return

    def loadWikiItem(self, witem):

        if self.langStr == 'en':
            self.pp.witem = witem
            self.pp.raw = witem.text
            self.pp.wcode = witem.wikicode
        # self.pp.cont = self.pp.wcode.filter_text()
        # self.pp.body = re.sub('<.*?>', '', self.pp.raw.replace("\n", ';;'))
        # self.pp.body = re.sub('<.*?>', '', self.pp.raw)
        if self.langStr == 'de':
            self.pp.witem = witem
            self.pp.raw = witem.text
            self.pp.wcode = witem.wikicode
            self.pp.cont = self.pp.wcode.filter_text()
            # prep text for regex processing
            self.pp.body = re.sub('[=:]', '', self.pp.raw.replace("\n",'').strip(':  '))
        return

    def returnProcessor(self):

        return self.pp

    def destroyProcessor(self):

        self.pp = None
