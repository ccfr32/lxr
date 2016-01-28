#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import subprocess

from files import Files
from index import Index
from lang import Lang
from simpleparse import PythonParse
from models import db, Tree, File, Symbol, LangType, Definitions, Ref
from ctags import ctags

class Genxref(object):

    def __init__(self, config, tree):
        self.files = Files(tree)
        self.filestype = {}
        self.tree = tree
        self.version = tree['version']
        self.treeid = Tree.query.get_treeid(tree['name'], tree['version'])

            
        self.config = config
        self.parse = PythonParse(config, tree)
        
        self.dfs_filetypes('.', self.version)
        # 建立swish
        self.gensearch(self.version)
        # ctags 符号
        self.symbols('.', self.version)
        # sym ref
        self.symref('.', self.version)

        
    def feedswish(self, pathname, version, swish):
        if self.files.isdir(pathname, version):
            dirs, files = self.files.getdir(pathname, version)
            for i in dirs + files:
                self.feedswish(os.path.join(pathname, i),
                               version,
                               swish)
        else:
            # filelist.write('%s\n' % pathname)
            if self.files.getsize(pathname, version) > 0:
                fp = self.files.getfp(pathname, version)
                content = fp.read()
                swish_input = [
                    "Path-Name: %s\n" % pathname,
                    "Content-Length:  %s\n" % len(content),
                    "Document-Type: TXT\n",
                    "\n",
                    content]
            
                swish.stdin.write(''.join(swish_input))
                fp.close()
                
                
    def gensearch(self, version):
        index_file = "%s.%s.index" % (self.tree['name'], version)
        index_file = os.path.join(self.config['swishdirbase'], index_file)
        cmd = '%s -S prog -i stdin -v 1 -c %s -f %s' % (
            self.config['swishbin'],
            self.config['swishconf'],
            index_file)
        swish = subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=True)
        self.feedswish('.', version, swish)
        out, err = swish.communicate()


    def dfs_filetypes(self, pathname, version):
        if self.files.isdir(pathname, version):            
            dirs, files = self.files.getdir(pathname, version)
            for i in dirs + files:
                self.dfs_filetypes(os.path.join(pathname, i), version)
        else:
            filetype = self.files.gettype(pathname, version)
            filename = self.files.toreal(pathname, version)
            self.filestype[filename] = filetype

            
    def symbols(self, pathname, version):

        if self.files.isdir(pathname, version):
            dirs, files = self.files.getdir(pathname, version)
            for i in dirs + files:
                self.symbols(os.path.join(pathname, i), version)
        else:
            _realfile = self.files.toreal(pathname, version)
            if _realfile in self.filestype:
                if self.filestype[_realfile] != 'python':
                    return
                o = File.query.get_or_create(self.treeid, pathname)
                if not o.has_indexed():
                    tags = ctags(_realfile, self.parse.lang)
                    for tag in tags:
                        sym, line, lang_type, ext = tag
                        symbol_obj = Symbol.query.get_or_create(self.treeid, sym)
                        lang_desc = self.parse.typemap[lang_type]
                        langtype_obj = LangType.query.get_or_create(self.parse.lang, lang_desc)
                        defin = Definitions(symbol_obj.symid, o.fileid, line, langtype_obj.typeid, ext)
                        db.session.add(defin)
                    o.set_indexed()
                    db.session.add(o)
            db.session.commit()
                
            
    def symref(self, pathname, version):
        if self.files.isdir(pathname, version):
            dirs, files = self.files.getdir(pathname, version)
            for i in dirs + files:
                self.symref(os.path.join(pathname, i), version)
        else:
            _realfile = self.files.toreal(pathname, version)
            if _realfile in self.filestype:
                if self.filestype[_realfile] != 'python':
                    return
                o = File.query.get_or_create(self.treeid, pathname)
                if not o.has_refered():
                    _fp = open(_realfile)
                    _buf = _fp.read()
                    _fp.close()
                    words = self.parse.get_idents(_buf)
                    for word, line in words:
                        symbol_obj = Symbol.query.get_or_create(self.treeid, word)
                        ref = Ref(symbol_obj.symid, o.fileid, line)
                        db.session.add(ref)
                    o.set_refered()
                    db.session.add(o)
            db.session.commit()

                    
if __name__ == "__main__":
    from conf import config, trees

    tree = trees['sqlalchemy']
    g = Genxref(config, tree)

