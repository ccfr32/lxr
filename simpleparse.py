#!/usr/bin/env python

import sys
import re

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
        html = '''<a class='fline' name="%s">%s</a>''' % line
        return html
    
    def out(self):
        htmls = ['<pre class="filecontent">']
        
        for fragtype, frag in self.frags:
            if fragtype == 'comment':
                htmls.append('')
            elif fragtype == 'string':
                htmls.append('')
            elif fragtype == 'include':
                htmls.append('')
            elif fragtype == 'code':
                htmls.append('')
            else:
                htmls.append('')
        htmls.append('</pre>')
        return ''.join(htmls)
    
    

class PythonParse(SimpleParse):

    langid = 27
    identdef = '[a-zA-Z]\w+'
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
    
    def __init__(self, buf):
        self.pos = 0
        self.buf = buf
        self.start = 0
        self.end = 0
        self.maxchar = len(buf)

        self.frags = []
        
        self.open_re = re.compile("|".join(['(%s)' % i['open'] for i in self.spec]), re.M)
        self.parse()

        _result = ''.join([i[1] for i in self.frags])
        assert _result == buf

        
    def parse(self):
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
        

                
if __name__ == "__main__":
    for filename in sys.argv[1:]:
        print filename
        fp = open(filename)
        buf = fp.read()
        fp.close()
        parse = PythonParse(buf)

    
        
        


            
            
