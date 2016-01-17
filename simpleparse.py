#!/usr/bin/env python

from conf import syntaxs
import re
class SimpleParse(object):
    
    def __init__(self, buf, lang):
        self.pos = 0
        self.buf = buf
        self.start = 0
        self.end = 0
        self.maxchar = len(buf)
        

        self.frags = []
        self.in_commnet = False
        self.in_string = False
        self.in_include = False
        self.lang = lang
        self.open_re = re.compile("|".join(['(%s)' % spec['open'] for spec in lang['spec']]), re.M)
        self.parse()

        _result = ''.join([i[1] for i in self.frags])
        assert _result == buf

        
    def parse(self):
        while self.pos < self.maxchar:
            match = self.open_re.search(self.buf, self.pos, self.maxchar)
            if match:
                left, right = match.start(), match.end()
                
                if self.pos < left:
                    frag = self.buf[self.pos:left]
                    self.frags.append(('code', frag))

                frag = self.buf[left:right]
                self.frags.append(('string', frag))

                self.pos = right
            else:
                frag = self.buf[self.pos:]
                self.frags.append(('code', frag))

                self.pos = self.maxchar
        

if __name__ == "__main__":
    #fp = open("/Users/yahuayan/work/github/lxr/data/source/redis-py/2.4/tests/lock.py")
    fp = open("/tmp/t.py")
    buf = fp.read()
    lang = syntaxs['python']
    parse = SimpleParse(buf, lang)

    
        
        


            
            
