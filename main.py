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
import conf
define("port", default=8888, help="run on the given port", type=int)

class MainHandler(tornado.web.RequestHandler):

    
    def prepare(self):
        self.page = None
        self.page_text = ''
        self.request_file = None
        self.current_tree = None
        self.releaseid = '2.4'
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

    def return_ident_page(self):
        self.render("ident.html", **self.detail)

    def _calc_source_content(self):
        if not self.request_file or self.request_file.endswith("/"):
            dirs, files = self.current_tree.getdir(self.request_file, self.releaseid)
            if not dirs and not files:
                return '''<p class="error">\n<i>The directory /%s does not exist, is empty or is hidden by an exclusion rule.</i>\n</p>\n''' % self.request_file

            res = []
            _count = 0
            for dir_name in dirs:
                i = {}
                i['dirclass'] = 'dirrow%d' % (_count%2 + 1)
                i['iconlink'] = ''
                i['namelink'] = dir_name
                i['filesize'] = ''
                i['modtime'] = ''
                i['desc'] = ''
                _count += 1
                res.append(i)
            for file_name in files:
                i = {}
                i['dirclass'] = 'dirrow%d' % (_count%2 + 1)
                i['iconlink'] = ''
                i['namelink'] = file_name
                i['filesize'] = ''
                i['modtime'] = ''
                i['desc'] = ''
                _count += 1
                res.append(i)
            loader = template.Loader(self.settings['template_path'])
            html = loader.load('htmldir.html').generate(files=res, desc='')
            return html
            
        return ''
        

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
        self.current_tree = Files(conf.trees.get(args[1]))
        if len(args) >= 3:
            if args[2].startswith("/"):
                self.request_file = args[2][1:]
            else:
                self.request_file = args[2]
        else:
            self.request_file = ''
        self.detail['request_file'] = self.request_file
        self.detail['current_tree'] = self.current_tree
        self.detail['current_page'] = self.page
        if self.page == 'search':
            self.return_search_page()
        elif self.page == 'ident':
            self.return_ident_page()
        elif self.page == 'source':
            self.return_source_page()
        else:
            self.return_index_page()


def main():
    app = tornado.web.Application(
        [(r"/lxr/(\w+)/(\w+)(/.*)?", MainHandler),],
        cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        template_path=os.path.join(os.path.dirname(__file__), "temp/html"),
        static_path=os.path.join(os.path.dirname(__file__), "temp"),
        xsrf_cookies=True,
        debug=True,
        )

    http_server = httpserver.HTTPServer(app)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
