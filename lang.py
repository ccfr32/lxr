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
        
    def indexfile(self):
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
            
        return 0

    def referencefile(self):
        return None


    
