#!/usr/bin/env python

import sys
import re
from index import Index
def find_escape_char(s, right, left):
    c = 0
    while right > left:
        if s[right] != '\\':
            break
        c += 1
        right -= 1
    if c % 2 == 0:
        return False
    return True

            
class SimpleParse(object):

    def get_line_html(self, line, width=4):
        line = '%04d' % line
        html = '''<a class='fline' name="%s">%s</a> ''' % (line, line)
        return html


    def _multilinetwist(self, frag, css):
        ss = '''<span class="%s">%s</span>''' % (css, frag)
        ss = ss.replace("\n", '</span>\n<span class="%s">' % css)
        ss = ss.replace('<span class="%s"></span>' % css, '')
        return ss
    


    def get_ident_link(self, ident):
        html = '''<a class='fid' href="/lxr/ident/redispy?_i=%s">%s</a>''' % (ident, ident)
        return html

    def get_reserved_link(self, word):
        if self.is_reserved(word):
            return '<span class="reserved">%s</span>' % word
        return word

    def is_ident(self, word):
        symid, symcount = self.index.symbols_byname(word)
        print word, symid, symcount
        if symid is not None:
            return True
        return False
    
    def is_reserved(self, word):
        return word in self.reserved
    
    def _parse_code(self, frag):
        ss = self.identdef.split(frag)
        kk = []
        for i in ss:
            if not i:
                continue
            if self.is_reserved(i):
                kk.append(self.get_reserved_link(i))
            elif self.is_ident(i):
                kk.append(self.get_ident_link(i))
            else:
                kk.append(i)
        return ''.join(kk)

    
    def out(self):
        head = '<pre class="filecontent">'
        tail = '</pre>'

        htmls = []
        for fragtype, frag in self.frags:
            if fragtype == 'comment':
                htmls.append(self._multilinetwist(frag, fragtype))
            elif fragtype == 'string':
                htmls.append(self._multilinetwist(frag, fragtype))
            elif fragtype == 'include':
                htmls.append(self._multilinetwist(frag, fragtype))
            elif fragtype == 'code':
                htmls.append(self._parse_code(frag))
            else:
                htmls.append(self._parse_code(frag))
        tt = ''.join(htmls).split("\n")
        linewidth = max(len(str(len(tt))), 4)
        
        line = 1
        htmls = [self.get_line_html(line, linewidth)]
        for i in tt:
            htmls.append(i)
            htmls.append('\n')
            line += 1
            htmls.append(self.get_line_html(line, linewidth))
        htmls.insert(0, head)
        htmls.append(tail)
        return ''.join(htmls)
        
    

class PythonParse(SimpleParse):

    langid = 27
    identdef = re.compile('([a-zA-Z]\w+)', re.M)
    reserved = ['and', 'as', 'assert', 'break', 'class', 'continue', 'def',
                'del', 'elif', 'else', 'except', 'exec', 'False', 'finally', 'for',
                'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'None', 'not',
                'or', 'pass', 'print', 'raise', 'return', 'self', 'True', 'try',
                'while', 'with', 'yield']
    spec = [
        {'open': '#', 'close': '\n', 'type': 'comment'},
        {'open': '"""', 'close': '"""', 'type': 'string'},
        {'open': "'''", 'close': "'''", 'type': 'string'},
        {'open': '"', 'close': '"', 'type': 'string'},
        {'open': "'", 'close': "'", 'type': 'string'},
        {'open': "\\bimport\\b", 'close': '\n', 'type': 'include'},
        {'open': "\\bfrom\\b", 'close': '\n', 'type': 'include'}
    ]
        
    typemap = {
        'c': 'class',
        'f': 'function',
        'i': 'import',
        'm': 'class member',
        'v': 'variable'
    }
    
    def __init__(self, config, tree):
        self.config = config
        self.tree = tree
        self.index = Index(config, tree)
        self.buf = []
        self.pos = 0
        self.start = 0
        self.end = 0
        self.maxchar = 0

        self.frags = []
        
        self.open_re = re.compile("|".join(['(%s)' % i['open'] for i in self.spec]), re.M)

        
    def parse(self, buf):
        self.buf = buf
        self.pos = 0
        self.start = 0
        self.end = 0
        self.maxchar = len(buf)

        self.frags = []
        

        
        while self.pos < self.maxchar:
            open_match = self.open_re.search(self.buf, self.pos, self.maxchar)
            if open_match:
                left, right = open_match.start(), open_match.end()
                if self.pos < left:
                    frag = self.buf[self.pos:left]
                    self.frags.append(('code', frag))

                match_groups = open_match.groups()
                i = 0
                while i < len(match_groups):
                    if match_groups[i]:
                        break
                    i += 1
                fragtype = self.spec[i]['type']
                close_re = self.spec[i]['close']
                close_left = self.buf.find(close_re, right, self.maxchar)
                # last line without newline
                if close_left < 0:
                    frag = self.buf[left:]
                    self.frags.append((fragtype, frag))
                    break
                close_right = close_left + len(close_re)
                if close_re == '"' or close_re == "'":
                    while find_escape_char(self.buf, close_left - 1, right - 1):
                        close_left = self.buf.find(close_re, close_right, self.maxchar)
                        # ERROR, break
                        if close_left < 0:
                            close_right = self.maxchar
                            print 'ERROR.'
                            break
                        close_right = close_left + len(close_re)

                frag = self.buf[left:close_right]
                self.frags.append((fragtype, frag))
                self.pos = close_right
            else:
                frag = self.buf[self.pos:]
                self.frags.append(('code', frag))
                self.pos = self.maxchar
    
        _result = ''.join([i[1] for i in self.frags])
        assert _result == buf


                
if __name__ == "__main__":
    from conf import config, trees
    for filename in sys.argv[1:]:
        print filename
        fp = open(filename)
        buf = fp.read()
        fp.close()
        parse = PythonParse(config, trees['redispy'])
        parse.parse(buf)

    
        
        


            
            
