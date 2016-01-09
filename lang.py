#!/usr/bin/env python

import subprocess

class Lang(object):

    def __init__(self, pathname, releaseid, files, index, config):
        self.files = files
        self.index = index
        self.config = config
        self.pathname = pathname
        self.releaseid = releaseid
        self.realpath = files.toreal(pathname, releaseid)
        self.lang = 'Python'
        self.langid = 7
        
    def indexfile(self, fileid):
        cmd = '%s %s --excmd=number --language-force=%s -f - %s' %(
            self.config['ectagsbin'], self.config['ectagsopts'],
            self.lang, self.realpath)
        print cmd
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, err = process.communicate()
        if not out:
            return 0
        lines = out.split("\n")
        for li in lines:
            if not li:
                continue
            values = li.rstrip().split("\t")
            print li
            if len(values) == 5:
                c_sym, c_file, c_line, c_type, c_ext = values
            elif len(values) == 4:
                c_sym, c_file, c_line, c_type = values
                c_ext = None
            else:
                print len(values)
            #self.index.setsymdeclaration(c_sym, fileid, c_line, self.langid, c_type, c_ext);
        return 0

    def referencefile(self, fileid):

        refs = []

        for string, line_no in refs:
            self.index.setsymreference(string, fileid, line_no)



    def multilinetwist(self, frag, css):
        html = '<span class="%s">%s</span>' % (css, frag)
        html = html.replace("\n", '</span>\n<span class="%s">' % css)
        html = html.replace('<span class="%s"></span>' % css, '')
        return html

    def processcomment(self, frag, css):
        return self.multilinetwist(frag, css)

    def processstring(self, frag, css):
        return self.multilinetwist(frag, css)

    def processextra(self, frag, css):
        return self.multilinetwist(frag, css)

    def processinclude(self, frag, dirname):
        pass

    def processcode(self, frag):
        pass
    
    def isreserved(self, frag):
        return frag in self.syntax['reserved']
    
    
            
    
