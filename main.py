#!/usr/bin/env python
import logging
import tornado.escape
import tornado.ioloop
import tornado.web
import os.path
import uuid

from tornado import httpserver
from tornado.concurrent import Future
from tornado import gen
from tornado.options import define, options, parse_command_line
from tornado import template

from files import Files
from simpleparse import PythonParse
import conf
from index import Index
from models import Symbol, Ref, Definitions

from dbcache import treecache, langcache, filecache, symbolcache

symbolcache.load(1)
filecache.load(1)

define("port", default=8888, help="run on the given port", type=int)

class MainHandler(tornado.web.RequestHandler):
    
    def prepare(self):
        self.page = None
        self.page_text = ''
        self.reqfile = None
        self.tree = None
        self.files = None
        self.tree_id = None
        self.releaseid = ''
        self.detail = {}
        self.detail['trees'] = self.get_all_trees()
        self.detail['pages'] = {
            'source': 'Source navigation',
            'ident': 'Identifier search',
            'search': 'General search'
        }
        

    def get_all_trees(self):
        return conf.trees.values()

    
    def get_swish_search(self, search_text):
        return []


    def _identfile(self, filename):
        return '''<a class="identfile" href="/lxr/source/%s%s">%s</a>''' % (
            self.tree['name'], filename, filename)

    def _identline(self, filename, line):
        return '''<a class="identline" href="/lxr/source/%s%s#%04d">%d</a>''' % (
            self.tree['name'], filename, line, line)
    
    def return_ident_page(self):
        ident = self.get_argument('_i')

        symid = symbolcache.get_symid(self.tree_id, ident)
        if symid is None:
            symbolcache.load(self.tree_id)
            symid = symbolcache.get_symid(self.tree_id, ident)
        if not symid:
            defs = []
            refs = []
        else:
            objs = Definitions.query.filter(Definitions.symid==symid).all()
            defs = []
            for o in objs:
                lang, desc = langcache.get_lang_desc(o.typeid)
                if lang is None and desc is None:
                    langcache.load()
                lang, desc = langcache.get_lang_desc(o.typeid)

                treeid, filename = filecache.get_treeid_filename(o.fileid)
                if treeid is None and filename is None:
                    filecache.load(self.tree_id)
                    treeid, filename = filecache.get_treeid_filename(o.fileid)
                defs.append(
                    (desc,
                     self._identfile(filename),
                     self._identline(filename, o.line)
                    )
                )

            objs = Ref.query.filter(Ref.symid==symid).all()
            refs = []
            for o in objs:
                treeid, filename = filecache.get_treeid_filename(o.fileid)
                if treeid is None and filename is None:
                    filecache.load(self.tree_id)
                    treeid, filename = filecache.get_treeid_filename(o.fileid)
                refs.append(
                    (self._identfile(filename),
                     self._identline(filename, o.line)
                    )
                )
        self.detail['defs'] = defs
        self.detail['refs'] = refs
        self.detail['ident'] = ident
        self.render("ident.html", **self.detail)

    def _calc_dir_content(self):
        dirs, files = self.files.getdir(self.reqfile, self.releaseid)
        if not dirs and not files:
            return '''<p class="error">\n<i>The directory /%s does not exist, is empty or is hidden by an exclusion rule.</i>\n</p>\n''' % self.reqfile
        
        res = []
        _count = 0
        if self.reqfile != '/':
            i = {}
            i['name'] = "Parent directory"
            i['class'] = 'dirfolder'
            i['dirclass'] = 'dirrow%d' % (_count%2 + 1)
            i['href'] = "/lxr/source/%s%s" % (self.tree['name'], os.path.dirname(self.reqfile))
            i['img'] = '/icons/back.gif'
            i['filesize'] = '-'
            i['modtime'] = '-'
            i['desc'] = ''
            _count += 1
            res.append(i)
            

        for dir_name in dirs:
            i = {}
            i['name'] = dir_name + "/"
            i['class'] = 'dirfolder'
            i['dirclass'] = 'dirrow%d' % (_count%2 + 1)
            if self.reqfile and self.reqfile != '/':
                i['href'] = "/lxr/source/%s%s/%s" % (self.tree['name'], self.reqfile, dir_name)
            else:
                i['href'] = "/lxr/source/%s/%s" % (self.tree['name'], dir_name)
            i['img'] = '/icons/folder.gif'
            i['filesize'] = '-'
            i['modtime'] = '-'
            i['desc'] = ''
            _count += 1
            res.append(i)
        for file_name in files:
            i = {}
            i['name'] = file_name
            i['class'] = 'dirfile'
            i['dirclass'] = 'dirrow%d' % (_count%2 + 1)
            if self.reqfile != '/':
                i['href'] = "/lxr/source/%s%s/%s" % (self.tree['name'], self.reqfile, file_name)
            else:
                i['href'] = "/lxr/source/%s/%s" % (self.tree['name'], file_name)
            i['img'] = '/icons/generic.gif'
            i['filesize'] = '-'
            i['modtime'] = '-'
            i['desc'] = ''
            _count += 1
            res.append(i)
        loader = template.Loader(self.settings['template_path'])
        html = loader.load('htmldir.html').generate(files=res, desc='')
        return html

    def _calc_code_file(self):
        if self.reqfile.lower().endswith(".py"):
            parse = PythonParse(conf.config, self.tree)
            parse.parse_file(self.reqfile, self.releaseid)
            return parse.out()
        return self._calc_raw_file()
    
    def _calc_raw_file(self):
        html = '''<pre class="filecontent">'''
        fp = self.files.getfp(self.reqfile, self.releaseid)
        lineno = 0
        for li in fp:
            lineno += 1
            html += '''<a class='fline' name="%04d">%04d</a> %s''' % (lineno, lineno, li)
        fp.close()
        html += '''</pre>'''
        return html

    def _calc_source_content(self):
        if self.files.isdir(self.reqfile, self.releaseid):
            return self._calc_dir_content()
        elif self.files.parseable(self.reqfile, self.releaseid):
            return self._calc_code_file()
        else:
            return self._calc_raw_file()

    def return_source_page(self):
        self.detail['source_content'] = self._calc_source_content()
        self.render("source.html", **self.detail)
    
    def return_search_page(self):
        self.detail['filetext'] = self.get_argument('filetext', '')
        self.detail['searchtext'] = self.get_argument('searchtext', '')
        self.detail['results'] = self.get_swish_search('')
        self.detail['advancedchecked'] = self.get_argument('advancedchecked', '')
        self.detail['casesensitivechecked'] = self.get_argument('casesensitivechecked', '')
        self.render("search.html", **self.detail)
        

    def return_index_page(self):
        self.render("index.html", **self.detail)
        
    def get(self, *args):
        self.page = args[0]
        self.tree = conf.trees.get(args[1])
        self.tree_id = treecache.get_treeid(self.tree['name'], self.tree['version'])
        self.releaseid = self.tree['version']
        self.files = Files(conf.trees.get(args[1]))

        if len(args) >= 3:
            self.reqfile = args[2] or '/'
        else:
            self.reqfile = '/'
        self.detail['tree'] = self.tree
        self.detail['reqfile'] = self.reqfile
        self.detail['files'] = self.files
        self.detail['page'] = self.page
        if self.page == 'search':
            self.return_search_page()
        elif self.page == 'ident':
            self.return_ident_page()
        elif self.page == 'source':
            self.return_source_page()
        else:
            self.return_index_page()

        
            
def main():
    tornado.options.parse_command_line()
    settings = dict(
        cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        template_path=os.path.join(os.path.dirname(__file__), "temp/html"),
        static_path=os.path.join(os.path.dirname(__file__), "temp"),
        xsrf_cookies=True,
        debug=False,
    )

    mapping = [
        (r"/lxr/(\w+)/(\w+)(/.*)?", MainHandler),
        (r"/icons/(.+)", tornado.web.StaticFileHandler, dict(path=settings['static_path']+"/icons/")),
    ]
    app = tornado.web.Application(
        mapping, **settings
    )

    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
