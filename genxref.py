import os
import subprocess

from lib.source import SourceTree

class Genxref(object):

    def __init__(self, config, tree):
        self.st = SourceTree(tree)
        self.tree = tree
        self.config = config
        self.defult_releaseid = tree['variables']['v']['default']
        self.gensearch(self.defult_releaseid)
        
        
    def feedswish(self, pathname, releaseid, swish):
        if self.st.isdir(pathname, releaseid):
            dirs, files = self.st.getdir(pathname, releaseid)
            for i in dirs + files:
                self.feedswish(os.path.join(pathname, i),
                               releaseid,
                               swish)
        else:
            # filelist.write('%s\n' % pathname)
            if self.st.getsize(pathname, releaseid) > 0:
                fp = self.st.getfp(pathname, releaseid)
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
        index_file = "%s.%s.index" % (self.tree['treename'], releaseid)
        index_file = os.path.join(self.config['swishdirbase'], index_file)
        cmd = '%s -S prog -i stdin -v 1 -c %s -f %s' % (
            self.config['swishbin'],
            self.config['swishconf'],
            index_file)
        print cmd
        swish = subprocess.Popen(cmd, stdin=subprocess.PIPE, shell=True)
        self.feedswish('.', releaseid, swish)
        print swish.communicate()


if __name__ == "__main__":
    from .conf import config, trees

    tree = trees['redispy']
    g = Genxref(config, tree)

