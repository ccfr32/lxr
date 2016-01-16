#!/usr/bin/env python

class SimpleParse(object):

    def __init__(self, fp, tabhint, syntax_spec):
        self.frags = []
        self.next = None
        
        self.bodyid = []
        self.open = []
        self.term = []
        self.stay = []
        self.continue = None
        
        for k in syntax_spec:
            v = syntax_spec[k]
            if v == 'atom':
            self.bodyid.append(k)
            self.open.append(k[0])
            self.term.append(k[1])
            self.stay.append(k[2])
        
        self.fp = fp
        self.tabwidth = tabhint // 8;

                self.split = ''
        self.open = ''


        for i in self.open:
            self.open += "(%s)|" % i
            self.split += "%s|" % i
        self.open = self.open[:-1]
        self.open = "^[\xFF\n]*(?:%s)$" % self.open
        self.split = self.split[:-1]


    def nextfrag(self):

        btype = None
        frag = None
        term = None

        change = self.split
        stay = self.continue

        line = None
        opos = None
        spos = None
        
        while(True):

            if self.frags:
                self.next = self.frags.pop(0)

            if not self.next:
                line = self.fp.readline()
                if not line:
                    break
                self.next = '\xFF' + line

            if self.frag and not re.match(r"['\xff\n']*", self.frag):
                # not just newlines
                pass
            else:
                if self.next 
                
        if btype:
            btype = self.bodyid[btype]
        frag = None
                
            
