import os
import subprocess

from files import Files
from index import Index
from lang import Lang

class Genxref(object):

    def __init__(self, config, tree):
        self.files = Files(tree)
        self.filestype = {}
        self.tree = tree
        self.config = config
        self.default_releaseid = tree['default_version']
        self.dfs_filetypes('.', self.default_releaseid)
        self.index = Index(config, tree)
        self.gensearch(self.default_releaseid)
        self.dfs_process_file('.', self.default_releaseid)
     
        
        #self.dfs_process_refs('.', self.default_releaseid)

        
    def feedswish(self, pathname, releaseid, swish):
        if self.files.isdir(pathname, releaseid):
            dirs, files = self.files.getdir(pathname, releaseid)
            for i in dirs + files:
                self.feedswish(os.path.join(pathname, i),
                               releaseid,
                               swish)
        else:
            # filelist.write('%s\n' % pathname)
            if self.files.getsize(pathname, releaseid) > 0:
                fp = self.files.getfp(pathname, releaseid)
                content = fp.read()
                swish_input = [
                    "Path-Name: %s\n" % pathname,
                    "Content-Length:  %s\n" % len(content),
                    "Document-Type: TXT\n",
                    "\n",
                    content]
            
                swish.stdin.write(''.join(swish_input))
                fp.close()
                
                
    def gensearch(self, releaseid):
        index_file = "%s.%s.index" % (self.tree['name'], releaseid)
        index_file = os.path.join(self.config['swishdirbase'], index_file)
        cmd = '%s -S prog -i stdin -v 1 -c %s -f %s' % (
            self.config['swishbin'],
            self.config['swishconf'],
            index_file)
        swish = subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=True)
        self.feedswish('.', releaseid, swish)
        out, err = swish.communicate()



    def _processfile(self, pathname, releaseid):
        print 'processfile: %s' % self.files.toreal(pathname, releaseid)
        revision = self.files.filerev(pathname, releaseid)
        fileid = self.index.fileid(pathname, revision)
        #self.index.setfilerelease(fileid, releaseid)
        if not self.index.fileindexed(fileid):
            lang = Lang(pathname, releaseid, self.files, self.index, self.config)
            ns = lang.indexfile()
            #self.index.flushcache()
            self.index.setfileindexed(fileid)
        
        
    def _processrefs(self, pathname, releaseid, config, files, index):
        revision = files.filerev(pathname, releaseid)
        fileid = index.fileid(pathname, revision)
        
        if not index.filereferenced(fileid):
            lang = Lang(pathname, releaseid, self.files, self.index, self.config)
            ns = lang.referencefile()
            #index.flushcache()
            index.setfilereferenced(fileid)


    def dfs_filetypes(self, pathname, releaseid):
        if self.files.isdir(pathname, releaseid):            
            dirs, files = self.files.getdir(pathname, releaseid)
            for i in dirs + files:
                self.dfs_filetypes(os.path.join(pathname, i), releaseid)
        else:
            filetype = self.files.gettype(pathname, releaseid)
            filename = self.files.toreal(pathname, releaseid)
            self.filestype[filename] = filetype

            
    def dfs_process_file(self, pathname, releaseid):
        if self.files.isdir(pathname, releaseid):
            dirs, files = self.files.getdir(pathname, releaseid)
            for i in dirs + files:
                self.dfs_process_file(os.path.join(pathname, i), releaseid)
        elif self.filestype[self.files.toreal(pathname, releaseid)] != 'bin':
            self._processfile(pathname, releaseid)
                
            
    def dfs_process_refs(self, pathname, releaseid):
        if self.files.isdir(pathname, releaseid):
            dirs, files = self.files.getdir(pathname, releaseid)
            for i in dirs + files:
                self.dfs_process_refs(os.path.join(pathname, i), releaseid)
        elif self.filestype[self.files.toreal(pathname, releaseid)] != 'bin':
            self._processrefs(pathname, releaseid)
            
        

if __name__ == "__main__":
    from conf import config, trees

    tree = trees['redispy']
    g = Genxref(config, tree)

