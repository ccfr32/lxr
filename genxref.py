import os
import subprocess

from files import Files

class Genxref(object):

    def __init__(self, config, tree):
        self.files = Files(tree)
        self.filestype = {}
        self.tree = tree
        self.config = config
        self.default_releaseid = tree['default_version']
        self.dfs_filetypes('.', self.default_releaseid)
        for k, v in self.filestype.items():
            print k, v
        #self.gensearch(self.default_releaseid)
        #self.dfs_process_file('.', self.default_releaseid)
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
        print cmd
        swish = subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=True)
        self.feedswish('.', releaseid, swish)
        print swish.communicate()



    def _processfile(self, pathname, releaseid, config, files, index):
        revision = files.filerev(pathname, releaseid)
        fileid = index.fileid(pathname, revision)
        index.setfilerelease(fileid, releaseid)
        
        if not index.fileindexed(fileid):
            lang = Lang(pathname, releaseid)
            ns = lang.indexfile(pathname, path, fileid, index, config)
            index.flushcache()
            index.setfileindexed(fileid)
        
        
    def _processrefs(self, pathname, releaseid, config, files, index):
        revision = files.filerev(pathname, releaseid)
        fileid = index.fileid(pathname, revision)
        
        if not index.filereferenced(fileid):
            lang = Lang(pathname, releaseid)
            ns = lang.referencefile(pathname, path, fileid, index, config)
            index.flushcache()
            index.setfilereferenced(fileid)


    def dfs_filetypes(self, pathname, releaseid):
        print pathname, releaseid
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
                self.dfs_process_file(releaseid, pathname)
        elif self.filestype[self.files.toreal(pathname, releaseid)] != 'bin':
            self._processfile(pathname, releaseid)
                
            
    def dfs_process_refs(self, pathname, releaseid):
        if self.files.isdir(pathname, releaseid):
            dirs, files = self.files.getdir(pathname, releaseid)
            for i in dirs + files:
                self.dfs_process_refs(releaseid, pathname)
        elif self.filestype[self.files.toreal(pathname, releaseid)] != 'bin':
            self._processrefs(pathname, releaseid)
            
        

if __name__ == "__main__":
    from conf import config, trees

    tree = trees['redispy']
    g = Genxref(config, tree)

