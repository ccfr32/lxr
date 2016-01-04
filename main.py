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

define("port", default=8888, help="run on the given port", type=int)

class MainHandler(tornado.web.RequestHandler):

    def prepare(self):
        self.page = None
        self.page_text = ''
        self.current_tree = None
        self.releaseid = None
        self.detail = {}
        self.detail['trees'] = self.get_all_trees()
        self.detail['pages'] = {
            'source': 'Source navigation',
            'ident': 'Identifier search',
            'search': 'General search'
        }
        
    def get_all_trees(self):
        from conf import trees
        return trees.values()

    
    def get_swish_search(self, search_text):
        return []

    def return_ident_page(self):
        self.render("ident.html", **self.detail)
        

    def return_source_page(self):
        self.render("fatal.html", **self.detail)
    
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
        self.current_tree = args[1]
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
